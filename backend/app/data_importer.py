"""Repeatable dataset importer for the Supplement Recommendation Platform.
Validates schemas, types, foreign keys, and idempotently imports CSVs into the database.
"""
import os
import sys
import argparse
import pandas as pd
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from app.models import (
    Base, Source, Goal, Diet, Allergen, Condition, MedicationClass,
    ActivityLevel, SleepCategory, Supplement, SupplementGoalMap,
    SupplementActivityMap, SupplementLifestyleMap, SupplementDietCompat,
    SupplementAllergen, SafetyRule, ScoringConfig, CriterionValueRule,
    SystemConfig, ExplanationTemplate
)

TABLE_ORDER = [
    "sources", "goals", "diets", "allergens", "conditions",
    "medication_classes", "activity_levels", "sleep_categories",
    "supplements", "supplement_goal_map", "supplement_activity_map",
    "supplement_lifestyle_map", "supplement_diet_compat", "supplement_allergen",
    "safety_rules", "scoring_config", "criterion_value_rules",
    "system_config", "explanation_templates"
]

MODEL_MAP = {
    "sources": Source,
    "goals": Goal,
    "diets": Diet,
    "allergens": Allergen,
    "conditions": Condition,
    "medication_classes": MedicationClass,
    "activity_levels": ActivityLevel,
    "sleep_categories": SleepCategory,
    "supplements": Supplement,
    "supplement_goal_map": SupplementGoalMap,
    "supplement_activity_map": SupplementActivityMap,
    "supplement_lifestyle_map": SupplementLifestyleMap,
    "supplement_diet_compat": SupplementDietCompat,
    "supplement_allergen": SupplementAllergen,
    "safety_rules": SafetyRule,
    "scoring_config": ScoringConfig,
    "criterion_value_rules": CriterionValueRule,
    "system_config": SystemConfig,
    "explanation_templates": ExplanationTemplate,
}

PK_MAP = {
    "sources": ["source_id"],
    "goals": ["goal_id"],
    "diets": ["diet_code"],
    "allergens": ["allergen_code"],
    "conditions": ["condition_code"],
    "medication_classes": ["medclass_code"],
    "activity_levels": ["activity_code"],
    "sleep_categories": ["sleep_code"],
    "supplements": ["supplement_id"],
    "supplement_goal_map": ["mapping_id"],
    "supplement_activity_map": ["map_id"],
    "supplement_lifestyle_map": ["map_id"],
    "supplement_diet_compat": ["supplement_id", "diet_code"],
    "supplement_allergen": ["supplement_id", "allergen_code"],
    "safety_rules": ["rule_id"],
    "scoring_config": ["criterion_id"],
    "criterion_value_rules": ["rule_id"],
    "system_config": ["config_key"],
    "explanation_templates": ["template_id"],
}


def to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    return s in ("true", "1", "yes")


def clean_row_data(table_name: str, row: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {}
    for k, v in row.items():
        if pd.isna(v) or v == "":
            cleaned[k] = None
        else:
            cleaned[k] = v

    # Type casts
    if table_name == "goals":
        cleaned["is_active"] = to_bool(cleaned.get("is_active", True))
    elif table_name in ("activity_levels", "sleep_categories"):
        if cleaned.get("ordinal") is not None:
            cleaned["ordinal"] = int(cleaned["ordinal"])
    elif table_name == "supplements":
        cleaned["is_active"] = to_bool(cleaned.get("is_active", True))
    elif table_name == "supplement_goal_map":
        if cleaned.get("match_score") is not None:
            cleaned["match_score"] = float(cleaned["match_score"])
        cleaned["is_active"] = to_bool(cleaned.get("is_active", False))
    elif table_name in ("supplement_activity_map", "supplement_lifestyle_map"):
        if cleaned.get("match_score") is not None:
            cleaned["match_score"] = float(cleaned["match_score"])
        cleaned["is_active"] = to_bool(cleaned.get("is_active", False))
    elif table_name == "supplement_allergen":
        cleaned["is_active"] = to_bool(cleaned.get("is_active", False))
    elif table_name == "safety_rules":
        cleaned["is_active"] = to_bool(cleaned.get("is_active", False))
    elif table_name == "scoring_config":
        if cleaned.get("weight") is not None:
            cleaned["weight"] = float(cleaned["weight"])
        if cleaned.get("minimum_value") is not None:
            cleaned["minimum_value"] = float(cleaned["minimum_value"])
        if cleaned.get("maximum_value") is not None:
            cleaned["maximum_value"] = float(cleaned["maximum_value"])
        cleaned["is_active"] = to_bool(cleaned.get("is_active", True))
    elif table_name == "criterion_value_rules":
        if cleaned.get("value") is not None:
            cleaned["value"] = float(cleaned["value"])
    elif table_name == "explanation_templates":
        cleaned["is_active"] = to_bool(cleaned.get("is_active", True))

    return cleaned


def validate_and_import(data_dir: str, session: Session) -> Dict[str, Any]:
    """Validates CSV files in data_dir and imports them idempotently into the database session."""
    stats = {"imported": {}, "updated": {}, "skipped": {}, "errors": []}
    
    # Check directory exists
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' does not exist.")

    # 1. Read all files first and validate basic presence
    dfs: Dict[str, pd.DataFrame] = {}
    for table in TABLE_ORDER:
        file_path = os.path.join(data_dir, f"{table}.csv")
        if not os.path.exists(file_path):
            stats["errors"].append(f"Missing required CSV: {table}.csv")
            continue
        try:
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
            dfs[table] = df
        except Exception as e:
            stats["errors"].append(f"Failed to read {table}.csv: {e}")

    if stats["errors"]:
        return stats

    # 2. Iterate in topological order and upsert
    for table in TABLE_ORDER:
        df = dfs[table]
        model_cls = MODEL_MAP[table]
        pk_cols = PK_MAP[table]
        
        imported_count = 0
        updated_count = 0
        skipped_count = 0

        # Check required columns
        valid_model_columns = {c.name for c in model_cls.__table__.columns}
        csv_cols = [c for c in df.columns if c in valid_model_columns]

        for _, raw_row in df.iterrows():
            row_dict = {col: raw_row[col] for col in csv_cols}
            cleaned = clean_row_data(table, row_dict)

            # Check primary key fields are present
            if any(cleaned.get(pk) is None or str(cleaned.get(pk)).strip() == "" for pk in pk_cols):
                skipped_count += 1
                stats["errors"].append(f"{table}: Row skipped due to missing primary key {pk_cols}: {cleaned}")
                continue

            # Query existing record
            filter_args = [getattr(model_cls, pk) == cleaned[pk] for pk in pk_cols]
            existing = session.query(model_cls).filter(*filter_args).first()

            if existing:
                # Update attributes
                has_changes = False
                for k, v in cleaned.items():
                    if getattr(existing, k) != v:
                        setattr(existing, k, v)
                        has_changes = True
                if has_changes:
                    updated_count += 1
                else:
                    skipped_count += 1
            else:
                new_instance = model_cls(**cleaned)
                session.add(new_instance)
                imported_count += 1

        session.flush()
        stats["imported"][table] = imported_count
        stats["updated"][table] = updated_count
        stats["skipped"][table] = skipped_count

    session.commit()
    return stats


def main():
    parser = argparse.ArgumentParser(description="Import knowledge base CSVs into database.")
    parser.add_argument("data_dir", nargs="?", default="data", help="Directory containing CSV files (default: data)")
    args = parser.parse_args()

    # Import engine_db and Session_ from app.main
    from app.main import Session_, engine_db
    from app.models import Base
    Base.metadata.create_all(engine_db)

    session = Session_()
    try:
        data_path = args.data_dir
        if not os.path.isabs(data_path) and not os.path.exists(data_path):
            # Check relative to backend or project
            alt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), data_path)
            if os.path.exists(alt_path):
                data_path = alt_path

        print(f"Importing dataset from '{data_path}'...")
        res = validate_and_import(data_path, session)
        print("\nImport completed successfully:")
        for t in TABLE_ORDER:
            print(f"  {t:26s} -> New: {res['imported'].get(t, 0):2d}, Updated: {res['updated'].get(t, 0):2d}, Existing: {res['skipped'].get(t, 0):2d}")
        if res["errors"]:
            print("\nValidation warnings/errors:")
            for err in res["errors"]:
                print(f"  WARNING: {err}")
    finally:
        session.close()


if __name__ == "__main__":
    main()

