#!/usr/bin/env python3
"""Dataset Builder for Open Source Supplement Recommendation Platform.
Generates reproducible canonical CSV datasets in dataset/data/,
synchronizes with backend/data/, and updates backend/data_verified/.

Usage:
    python dataset/build.py [--sync-backend]
"""
import os
import sys
import csv
import shutil

# Ensure dataset package directory is on path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import supplement_data as sd

DATA_DIR = os.path.join(current_dir, "data")
BACKEND_DIR = os.path.join(os.path.dirname(current_dir), "backend")
BACKEND_DATA_DIR = os.path.join(BACKEND_DIR, "data")
BACKEND_VERIFIED_DIR = os.path.join(BACKEND_DIR, "data_verified")

T = sd.T_CREATED
RV = sd.RV


def write_csv(directory, filename, header, rows):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, f"{filename}.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def build_draft_dataset(target_dir):
    """Builds the canonical draft dataset. All candidate mappings are inactive & needs_review."""
    os.makedirs(target_dir, exist_ok=True)

    # 1. Reference Registries & Controlled Vocabularies
    write_csv(target_dir, "sources", ["source_id","source_name","source_type","url","access_method","reuse_note","limitations"], sd.SOURCES)
    write_csv(target_dir, "goals", ["goal_id","goal_code","goal_name","description","is_active"], sd.GOALS)
    write_csv(target_dir, "diets", ["diet_code","diet_name","description"], sd.DIETS)
    write_csv(target_dir, "allergens", ["allergen_code","allergen_name"], sd.ALLERGENS)
    write_csv(target_dir, "conditions", ["condition_code","condition_name","in_scope_note"], sd.CONDITIONS)
    write_csv(target_dir, "medication_classes", ["medclass_code","medclass_name","note"], sd.MEDICATION_CLASSES)
    write_csv(target_dir, "activity_levels", ["activity_code","activity_name","ordinal"], sd.ACTIVITY_LEVELS)
    write_csv(target_dir, "sleep_categories", ["sleep_code","sleep_name","ordinal"], sd.SLEEP_CATEGORIES)
    write_csv(target_dir, "status_definitions", ["status_value","applies_to","meaning"], sd.STATUS_DEFINITIONS)
    write_csv(target_dir, "scoring_config", ["criterion_id","criterion_code","criterion_name","weight","minimum_value","maximum_value","description","rule_version","is_active"], sd.SCORING_CONFIG)
    write_csv(target_dir, "system_config", ["config_key","config_value","description","rule_version"], sd.SYSTEM_CONFIG)
    write_csv(target_dir, "criterion_value_rules", ["rule_id","criterion_code","condition","value","note","rule_version"], sd.CRITERION_VALUE_RULES)
    write_csv(target_dir, "explanation_templates", ["template_id","criterion_code","match_value","template_text","required_attribute","rule_version","is_active"], sd.EXPLANATION_TEMPLATES)

    # 2. Supplements (All 130 records in draft state)
    sup_rows = []
    for sid, name, cat, desc, ing, forms, src_id, url, is_ver, notes in sd.SUPPLEMENT_RECORDS:
        sup_rows.append([
            sid, name, cat, desc, ing, forms, src_id, url,
            "needs_review", "", True, T, T, notes
        ])
    write_csv(target_dir, "supplements", [
        "supplement_id","supplement_name","supplement_category","description",
        "active_ingredients","ingredient_forms","primary_source_id","source_url",
        "verification_status","last_reviewed_at","is_active","created_at","updated_at","notes"
    ], sup_rows)

    # 3. Diet Compatibility (Draft scaffold: all unknown)
    diet_rows = []
    for sid, name, cat, desc, ing, forms, src_id, url, is_ver, notes in sd.SUPPLEMENT_RECORDS:
        for diet in ("vegetarian", "vegan"):
            diet_rows.append([
                sid, diet, "unknown", "", "", "needs_review", "",
                "Formulation dependent (capsule shell, carrier, source). Confirm from label."
            ])
    write_csv(target_dir, "supplement_diet_compat", [
        "supplement_id","diet_code","compat_status","source_id","source_ref",
        "verification_status","last_reviewed_at","notes"
    ], diet_rows)

    # 4. Goal Mappings (Draft: inactive & needs_review)
    goal_rows = []
    for mid, sid, gid, mtype, score, src_id, sref, notes, is_ver in sd.GOAL_MAPPINGS_DEF:
        goal_rows.append([
            mid, sid, gid, mtype, score, "", "",
            "PROPOSED candidate mapping; requires review against cited source before activation",
            "needs_review", RV, False
        ])
    write_csv(target_dir, "supplement_goal_map", [
        "mapping_id","supplement_id","goal_id","match_type","match_score",
        "source_id","source_ref","evidence_notes","verification_status","rule_version","is_active"
    ], goal_rows)

    # 5. Activity Mappings (Draft: inactive & needs_review)
    act_rows = []
    for mid, sid, code, mtype, score, src_id, sref, is_ver in sd.ACTIVITY_MAPPINGS_DEF:
        act_rows.append([
            mid, sid, code, mtype, score, "", "", "needs_review", RV, False
        ])
    write_csv(target_dir, "supplement_activity_map", [
        "map_id","supplement_id","activity_code","match_type","match_score",
        "source_id","source_ref","verification_status","rule_version","is_active"
    ], act_rows)

    # 6. Lifestyle / Sleep Mappings (Draft: inactive & needs_review)
    life_rows = []
    for mid, sid, code, mtype, score, src_id, sref, is_ver in sd.LIFESTYLE_MAPPINGS_DEF:
        life_rows.append([
            mid, sid, code, mtype, score, "", "", "needs_review", RV, False
        ])
    write_csv(target_dir, "supplement_lifestyle_map", [
        "map_id","supplement_id","sleep_code","match_type","match_score",
        "source_id","source_ref","verification_status","rule_version","is_active"
    ], life_rows)

    # 7. Allergen Mappings (Draft: inactive & needs_review)
    alg_rows = []
    for sid, allergen, relation, src_id, sref, is_ver, notes in sd.ALLERGEN_MAPPINGS_DEF:
        alg_rows.append([
            sid, allergen, relation, "", "", "needs_review", False, notes
        ])
    write_csv(target_dir, "supplement_allergen", [
        "supplement_id","allergen_code","relation","source_id","source_ref",
        "verification_status","is_active","notes"
    ], alg_rows)

    # 8. Safety Rules (Draft: R000 active, clinical rules inactive & needs_review)
    sr_rows = []
    for rid, sid, rtype, code, attr, action, reason, msg, src_id, sref, is_ver in sd.SAFETY_RULES_DEF:
        if rid == "R000":
            sr_rows.append([
                rid, sid, rtype, code, attr, action, reason, msg,
                src_id, sref, "not_applicable", RV, True
            ])
        else:
            sr_rows.append([
                rid, sid, rtype, code, attr, action, reason, msg,
                "", "", "needs_review", RV, False
            ])
    write_csv(target_dir, "safety_rules", [
        "rule_id","supplement_id","rule_type","condition_code","triggering_attribute",
        "action","reason","safety_message","source_id","source_ref",
        "verification_status","rule_version","is_active"
    ], sr_rows)

    print(f"Draft dataset successfully built in: {target_dir}")


def build_verified_dataset(src_dir, target_dir):
    """Builds the verified dataset from src_dir according to NIH ODS / NCCIH monographs."""
    os.makedirs(target_dir, exist_ok=True)

    # Copy base lookup tables
    for f in os.listdir(src_dir):
        if f.endswith(".csv"):
            shutil.copy2(os.path.join(src_dir, f), os.path.join(target_dir, f))

    # 1. Update supplements: verify well-documented supplements
    verified_map = {r[0]: r for r in sd.SUPPLEMENT_RECORDS}
    sup_rows = []
    for sid, name, cat, desc, ing, forms, src_id, url, is_ver, notes in sd.SUPPLEMENT_RECORDS:
        status = "verified" if is_ver else "needs_review"
        rev_date = T if is_ver else ""
        sup_rows.append([
            sid, name, cat, desc, ing, forms, src_id, url,
            status, rev_date, True, T, T, notes
        ])
    write_csv(target_dir, "supplements", [
        "supplement_id","supplement_name","supplement_category","description",
        "active_ingredients","ingredient_forms","primary_source_id","source_url",
        "verification_status","last_reviewed_at","is_active","created_at","updated_at","notes"
    ], sup_rows)

    # 2. Update Goal Mappings: activate verified mappings with authoritative citations
    gm_rows = []
    for mid, sid, gid, mtype, score, src_id, sref, notes, is_ver in sd.GOAL_MAPPINGS_DEF:
        status = "verified" if is_ver else "needs_review"
        gm_rows.append([
            mid, sid, gid, mtype, score,
            src_id if is_ver else "",
            sref if is_ver else "",
            notes, status, RV, is_ver
        ])
    write_csv(target_dir, "supplement_goal_map", [
        "mapping_id","supplement_id","goal_id","match_type","match_score",
        "source_id","source_ref","evidence_notes","verification_status","rule_version","is_active"
    ], gm_rows)

    # 3. Update Activity Mappings
    act_rows = []
    for mid, sid, code, mtype, score, src_id, sref, is_ver in sd.ACTIVITY_MAPPINGS_DEF:
        status = "verified" if is_ver else "needs_review"
        act_rows.append([
            mid, sid, code, mtype, score,
            src_id if is_ver else "",
            sref if is_ver else "",
            status, RV, is_ver
        ])
    write_csv(target_dir, "supplement_activity_map", [
        "map_id","supplement_id","activity_code","match_type","match_score",
        "source_id","source_ref","verification_status","rule_version","is_active"
    ], act_rows)

    # 4. Update Lifestyle / Sleep Mappings
    life_rows = []
    for mid, sid, code, mtype, score, src_id, sref, is_ver in sd.LIFESTYLE_MAPPINGS_DEF:
        status = "verified" if is_ver else "needs_review"
        life_rows.append([
            mid, sid, code, mtype, score,
            src_id if is_ver else "",
            sref if is_ver else "",
            status, RV, is_ver
        ])
    write_csv(target_dir, "supplement_lifestyle_map", [
        "map_id","supplement_id","sleep_code","match_type","match_score",
        "source_id","source_ref","verification_status","rule_version","is_active"
    ], life_rows)

    # 5. Update Allergen Mappings
    alg_rows = []
    for sid, allergen, relation, src_id, sref, is_ver, notes in sd.ALLERGEN_MAPPINGS_DEF:
        status = "verified" if is_ver else "needs_review"
        alg_rows.append([
            sid, allergen, relation,
            src_id if is_ver else "",
            sref if is_ver else "",
            status, is_ver, notes
        ])
    write_csv(target_dir, "supplement_allergen", [
        "supplement_id","allergen_code","relation","source_id","source_ref",
        "verification_status","is_active","notes"
    ], alg_rows)

    # 6. Update Diet Compatibility
    non_vegetarian = {"SUP044", "SUP045", "SUP061", "SUP127", "SUP128"}
    dairy_poultry = {"SUP053", "SUP054", "SUP055", "SUP060"}
    diet_rows = []
    for sid, name, cat, desc, ing, forms, src_id, url, is_ver, notes in sd.SUPPLEMENT_RECORDS:
        if is_ver:
            # Vegetarian
            if sid in non_vegetarian or sid == "SUP018":
                v_compat = "incompatible"
                v_notes = "Animal/marine tissue origin; not suitable for vegetarian diet."
            else:
                v_compat = "compatible"
                v_notes = "Suitable for vegetarian diets."

            # Vegan
            if sid in non_vegetarian:
                vg_compat = "incompatible"
                vg_notes = "Animal/marine origin; not suitable for vegan diet."
            elif sid in dairy_poultry:
                vg_compat = "incompatible"
                vg_notes = "Animal dairy/poultry origin; not suitable for vegan diet."
            elif sid == "SUP018":
                vg_compat = "depends_on_product"
                vg_notes = "Fish oil source is non-vegan; algal oil formulations are vegan."
            elif sid == "SUP019":
                vg_compat = "compatible"
                vg_notes = "Cultured probiotic strains in non-dairy broth."
            else:
                vg_compat = "compatible"
                vg_notes = "Plant/mineral/synthetic synthesis; suitable for vegan diets."

            diet_rows.append([sid, "vegetarian", v_compat, "SRC02", "DSLD Monograph", "verified", T, v_notes])
            diet_rows.append([sid, "vegan", vg_compat, "SRC02", "DSLD Monograph", "verified", T, vg_notes])
        else:
            # Unverified candidates
            diet_rows.append([sid, "vegetarian", "depends_on_product", "", "", "needs_review", "", "Candidate formulation; product-dependent."])
            diet_rows.append([sid, "vegan", "depends_on_product", "", "", "needs_review", "", "Candidate formulation; product-dependent."])

    write_csv(target_dir, "supplement_diet_compat", [
        "supplement_id","diet_code","compat_status","source_id","source_ref",
        "verification_status","last_reviewed_at","notes"
    ], diet_rows)

    # 7. Update Safety Rules: activate verified clinical & allergen rules
    sr_rows = []
    for rid, sid, rtype, code, attr, action, reason, msg, src_id, sref, is_ver in sd.SAFETY_RULES_DEF:
        if rid == "R000":
            sr_rows.append([
                rid, sid, rtype, code, attr, action, reason, msg,
                src_id, sref, "not_applicable", RV, True
            ])
        else:
            status = "verified" if is_ver else "needs_review"
            sr_rows.append([
                rid, sid, rtype, code, attr, action, reason, msg,
                src_id if is_ver else "",
                sref if is_ver else "",
                status, RV, is_ver
            ])
    write_csv(target_dir, "safety_rules", [
        "rule_id","supplement_id","rule_type","condition_code","triggering_attribute",
        "action","reason","safety_message","source_id","source_ref",
        "verification_status","rule_version","is_active"
    ], sr_rows)

    print(f"Verified dataset successfully built in: {target_dir}")


def main():
    print("=" * 60)
    print("Building Canonical Supplement Recommendation Platform Dataset")
    print("=" * 60)

    # 1. Build canonical draft dataset in dataset/data/
    build_draft_dataset(DATA_DIR)

    # 2. Synchronize to backend/data/
    if os.path.isdir(os.path.dirname(BACKEND_DATA_DIR)):
        print(f"Synchronizing to backend draft directory: {BACKEND_DATA_DIR}")
        build_draft_dataset(BACKEND_DATA_DIR)

    # 3. Build verified dataset in backend/data_verified/
    if os.path.isdir(os.path.dirname(BACKEND_VERIFIED_DIR)):
        print(f"Building verified dataset in: {BACKEND_VERIFIED_DIR}")
        build_verified_dataset(BACKEND_DATA_DIR, BACKEND_VERIFIED_DIR)

    print("\nDataset generation completed successfully across all targets.")


if __name__ == "__main__":
    main()
