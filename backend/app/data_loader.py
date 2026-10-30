"""Loads CSVs into the engine's KB. Only is_active AND verified rows are used."""
import pandas as pd
import os

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resolve(d: str) -> str:
    if os.path.isabs(d) and os.path.isdir(d):
        return d
    if os.path.isdir(d):
        return d
    alt = os.path.join(_backend_dir, d)
    if os.path.isdir(alt):
        return alt
    return d


def _r(d, n):
    path = os.path.join(_resolve(d), n + ".csv")
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")


def _ok(df):
    return df[(df.verification_status == "verified") & (df.is_active.str.lower() == "true")]


def load_kb(d="data"):
    cfg = dict(zip(*_r(d, "system_config")[["config_key", "config_value"]].values.T))
    sc = _r(d, "scoring_config")
    sc = sc[sc.is_active.str.lower() == "true"]
    sup = _r(d, "supplements")
    sup = sup[sup.is_active.str.lower() == "true"]
    dc = _r(d, "supplement_diet_compat")
    dc = dc[dc.verification_status == "verified"]
    return {
        "supps": {r.supplement_id: r._asdict() for r in sup.itertuples(index=False)},
        "goal": {(r.supplement_id, r.goal_id): float(r.match_score) for r in _ok(_r(d, "supplement_goal_map")).itertuples()},
        "act": {(r.supplement_id, r.activity_code): float(r.match_score) for r in _ok(_r(d, "supplement_activity_map")).itertuples()},
        "life": {(r.supplement_id, r.sleep_code): float(r.match_score) for r in _ok(_r(d, "supplement_lifestyle_map")).itertuples()},
        "diet": {(r.supplement_id, r.diet_code): r.compat_status for r in dc.itertuples()},
        "allergen": {(r.supplement_id, r.allergen_code) for r in _ok(_r(d, "supplement_allergen")).itertuples()},
        "rules": _ok(_r(d, "safety_rules")).to_dict("records") if len(_ok(_r(d, "safety_rules"))) else [],
        "weights": {r.criterion_code: float(r.weight) for r in sc.itertuples()},
        "threshold": float(cfg["threshold"]),
        "dataset_version": cfg["dataset_version"],
        "rule_version": cfg["dataset_version"],
        "scoring_version": cfg["scoring_version"],
        "templates": _r(d, "explanation_templates").to_dict("records")
    }
