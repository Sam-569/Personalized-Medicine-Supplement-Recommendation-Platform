#!/usr/bin/env python3
"""Validate the supplement knowledge-base CSVs.
Usage:
    python validate_dataset.py [data_dir] [--compare-with other_data_dir]

Exit code 1 if any ERROR. WARNINGs are informational (e.g. unverified candidates).
"""
import sys
import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Validate supplement knowledge base CSVs.")
parser.add_argument("data_dir", nargs="?", default="data", help="Directory containing CSV files to validate (default: data)")
parser.add_argument("--compare-with", dest="compare_dir", default=None, help="Optional second data directory to verify synchronization/consistency")
args = parser.parse_args()

D = args.data_dir
# Resolve relative to dataset directory if not found in cwd
if not os.path.exists(D):
    alt = os.path.join(os.path.dirname(os.path.abspath(__file__)), D)
    if os.path.exists(alt):
        D = alt

errors, warnings = [], []
E = lambda m: errors.append(m)
W = lambda m: warnings.append(m)

REQ = {
    "supplements": [
        "supplement_id", "supplement_name", "supplement_category", "description",
        "active_ingredients", "ingredient_forms", "primary_source_id", "source_url",
        "verification_status", "last_reviewed_at", "is_active", "created_at", "updated_at", "notes"
    ],
    "goals": ["goal_id", "goal_code", "goal_name", "is_active"],
    "supplement_goal_map": ["mapping_id", "supplement_id", "goal_id", "match_type", "match_score", "source_id", "verification_status", "rule_version", "is_active"],
    "supplement_activity_map": ["map_id", "supplement_id", "activity_code", "match_type", "match_score", "verification_status", "is_active"],
    "supplement_lifestyle_map": ["map_id", "supplement_id", "sleep_code", "match_type", "match_score", "verification_status", "is_active"],
    "supplement_diet_compat": ["supplement_id", "diet_code", "compat_status", "verification_status"],
    "supplement_allergen": ["supplement_id", "allergen_code", "verification_status", "is_active"],
    "safety_rules": ["rule_id", "supplement_id", "rule_type", "condition_code", "action", "safety_message", "source_id", "verification_status", "is_active"],
    "scoring_config": ["criterion_id", "criterion_code", "weight", "minimum_value", "maximum_value", "is_active"],
    "system_config": ["config_key", "config_value"],
    "criterion_value_rules": ["rule_id", "criterion_code", "condition", "value"],
    "explanation_templates": ["template_id", "criterion_code", "match_value", "template_text", "is_active"],
    "sources": ["source_id", "source_name", "url"],
    "diets": ["diet_code"],
    "allergens": ["allergen_code"],
    "conditions": ["condition_code"],
    "medication_classes": ["medclass_code"],
    "activity_levels": ["activity_code"],
    "sleep_categories": ["sleep_code"],
}
VSTAT = {"verified", "needs_review", "unknown", "not_applicable", "rejected"}
MATCH = {"direct": 1.0, "partial": 0.5, "none": 0.0}
ACTIONS = {"exclude", "require_review", "warn"}
RTYPES = {"allergy", "dietary", "condition", "interaction", "missing_info"}
COMPAT = {"compatible", "incompatible", "depends_on_product", "unknown"}

dfs = {}
for name, cols in REQ.items():
    p = os.path.join(D, f"{name}.csv")
    if not os.path.exists(p):
        E(f"missing file: {name}.csv")
        continue
    try:
        df = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8")
    except Exception as exc:
        E(f"{name}.csv: encoding or read error: {exc}")
        continue
    miss = [c for c in cols if c not in df.columns]
    if miss:
        E(f"{name}: missing columns {miss}")
        continue
    dfs[name] = df

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)


def b(s):
    return s.str.strip().str.lower().isin(["true", "1", "yes"])


def unique(name, col):
    d = dfs[name][col][dfs[name][col] != ""]
    dup = d[d.duplicated()].tolist()
    if dup:
        E(f"{name}.{col}: duplicate values {dup}")
    if (dfs[name][col] == "").any():
        E(f"{name}.{col}: empty value(s)")


def fk(name, col, ref, refcol, allow_blank=False):
    vals = dfs[name][col]
    if allow_blank:
        vals = vals[vals != ""]
    bad = sorted(set(vals) - set(dfs[ref][refcol]))
    if bad:
        E(f"{name}.{col}: values not in {ref}.{refcol}: {bad}")


def enum(name, col, allowed):
    bad = sorted(set(dfs[name][col]) - allowed)
    if bad:
        E(f"{name}.{col}: invalid values {bad}; allowed {sorted(allowed)}")


def num(name, col):
    s = pd.to_numeric(dfs[name][col], errors="coerce")
    if s.isna().any():
        E(f"{name}.{col}: non-numeric values at rows {list(s[s.isna()].index + 2)}")
    return s


def check_url(name, col):
    if col in dfs[name].columns:
        urls = dfs[name][col][dfs[name][col] != ""]
        bad = urls[~urls.str.startswith(("http://", "https://"))].tolist()
        if bad:
            E(f"{name}.{col}: invalid URL format (must begin with http:// or https://): {bad[:3]}")


# 1. Scale & Identifiers
n_supps = len(dfs["supplements"])
if n_supps < 100:
    E(f"supplements: catalogue must contain at least 100 distinct records; found {n_supps}")

# Preservation of foundational baseline IDs
base_ids = {f"SUP{i:03d}" for i in range(1, 25)}
missing_base = base_ids - set(dfs["supplements"].supplement_id)
if missing_base:
    E(f"supplements: missing foundational supplement IDs (SUP001-SUP024): {sorted(missing_base)}")

for n, c in [
    ("supplements", "supplement_id"),
    ("goals", "goal_id"),
    ("goals", "goal_code"),
    ("supplement_goal_map", "mapping_id"),
    ("supplement_activity_map", "map_id"),
    ("supplement_lifestyle_map", "map_id"),
    ("safety_rules", "rule_id"),
    ("scoring_config", "criterion_id"),
    ("scoring_config", "criterion_code"),
    ("sources", "source_id"),
    ("explanation_templates", "template_id"),
    ("criterion_value_rules", "rule_id"),
    ("system_config", "config_key"),
]:
    unique(n, c)

if dfs["supplements"].supplement_name.str.lower().duplicated().any():
    dup_names = dfs["supplements"][dfs["supplements"].supplement_name.str.lower().duplicated()].supplement_name.tolist()
    E(f"supplements: duplicate supplement_name: {dup_names}")

# 2. URLs & Source references
check_url("sources", "url")
check_url("supplements", "source_url")

# 3. Foreign Keys
for t in [
    "supplement_goal_map",
    "supplement_activity_map",
    "supplement_lifestyle_map",
    "supplement_diet_compat",
    "supplement_allergen",
]:
    fk(t, "supplement_id", "supplements", "supplement_id")

fk("safety_rules", "supplement_id", "supplements", "supplement_id", allow_blank=True)
fk("supplement_goal_map", "goal_id", "goals", "goal_id")
fk("supplement_activity_map", "activity_code", "activity_levels", "activity_code")
fk("supplement_lifestyle_map", "sleep_code", "sleep_categories", "sleep_code")
fk("supplement_diet_compat", "diet_code", "diets", "diet_code")
fk("supplement_allergen", "allergen_code", "allergens", "allergen_code")

for t in [
    "supplement_goal_map",
    "safety_rules",
    "supplement_diet_compat",
    "supplement_allergen",
    "supplement_activity_map",
    "supplement_lifestyle_map",
]:
    if "source_id" in dfs[t].columns:
        fk(t, "source_id", "sources", "source_id", allow_blank=True)

if "primary_source_id" in dfs["supplements"].columns:
    fk("supplements", "primary_source_id", "sources", "source_id", allow_blank=True)

ok_conditions = (
    set(dfs["conditions"].condition_code)
    | set(dfs["medication_classes"].medclass_code)
    | set(dfs["allergens"].allergen_code)
    | set(dfs["diets"].diet_code)
    | {"ANY"}
)
bad_conditions = sorted(set(dfs["safety_rules"].condition_code) - ok_conditions)
if bad_conditions:
    E(f"safety_rules.condition_code: unknown codes {bad_conditions}")

# 4. Enums / match values
for t in [
    "supplements",
    "supplement_goal_map",
    "supplement_activity_map",
    "supplement_lifestyle_map",
    "supplement_diet_compat",
    "supplement_allergen",
    "safety_rules",
]:
    enum(t, "verification_status", VSTAT)

enum("safety_rules", "action", ACTIONS)
enum("safety_rules", "rule_type", RTYPES)
enum("supplement_diet_compat", "compat_status", COMPAT)

for t in ["supplement_goal_map", "supplement_activity_map", "supplement_lifestyle_map"]:
    enum(t, "match_type", set(MATCH))
    s = num(t, "match_score")
    for mt, v in MATCH.items():
        sub = s[dfs[t].match_type == mt]
        if (sub.sub(v).abs() > 1e-9).any():
            E(f"{t}: match_score inconsistent with match_type={mt} (expected {v})")

# 5. Scoring weights / bounds
sc = dfs["scoring_config"]
act = sc[b(sc.is_active)]
w_ = pd.to_numeric(act.weight, errors="coerce")
if w_.isna().any():
    E("scoring_config.weight non-numeric")
elif abs(w_.sum() - 1.0) > 1e-9:
    E(f"active weights sum to {w_.sum()}, expected 1.00")
if (w_ < 0).any() or (w_ > 1).any():
    E("weights must be within [0,1]")
if not (pd.to_numeric(sc.minimum_value).eq(0).all() and pd.to_numeric(sc.maximum_value).eq(1).all()):
    E("criterion min/max must be 0 and 1")
if set(act.criterion_code) != {"G", "D", "A", "L", "H"}:
    E(f"active criteria must be G,D,A,L,H; got {sorted(set(act.criterion_code))}")

cv = pd.to_numeric(dfs["criterion_value_rules"].value, errors="coerce")
if cv.isna().any() or (cv < 0).any() or (cv > 1).any():
    E("criterion_value_rules.value must be numeric in [0,1]")
fk("criterion_value_rules", "criterion_code", "scoring_config", "criterion_code")

cfg = dict(zip(dfs["system_config"].config_key, dfs["system_config"].config_value))
try:
    t_val = float(cfg["threshold"])
    assert 0 <= t_val <= 1
except Exception:
    E("system_config.threshold missing or not in [0,1]")

# 6. Safety-sensitive rows: sources + review status
def need_source(t, flag_active_unverified=True):
    df = dfs[t]
    ver = df.verification_status == "verified"
    if "source_id" in df.columns:
        nosrc = df[ver & (df.source_id == "")]
        if len(nosrc):
            E(f"{t}: verified rows without source_id")
    if flag_active_unverified and "is_active" in df.columns:
        bad = df[b(df.is_active) & ~ver & (df.verification_status != "not_applicable")]
        if len(bad):
            E(f"{t}: {len(bad)} ACTIVE rows are not verified (engine must only use verified rows)")
    n = (~ver).sum()
    if n:
        W(f"{t}: {n} of {len(df)} rows not verified yet (needs_review/unknown)")


for t in [
    "supplement_goal_map",
    "supplement_activity_map",
    "supplement_lifestyle_map",
    "safety_rules",
    "supplement_allergen",
]:
    need_source(t)

need_source("supplement_diet_compat", flag_active_unverified=False)

sr = dfs["safety_rules"]
if (sr.safety_message == "").any():
    E("safety_rules: empty safety_message")

if not (
    sr.rule_id.isin(["R000"])
    & (sr.condition_code == "ANY")
    & (sr.action == "require_review")
).any():
    E("safety_rules: missing default 'missing_info' rule (R000) that requires review when safety info is unverified")

# 7. Unverified safety info must route to review
sup = dfs["supplements"]
ver_safe = set(sr[(sr.verification_status == "verified") & b(sr.is_active)].supplement_id)
unsafe = sorted(set(sup[b(sup.is_active)].supplement_id) - ver_safe)
if unsafe:
    W(f"{len(unsafe)} active supplements have NO verified safety rule -> engine routes them to require_review/withhold (Rule R000)")

dc = dfs["supplement_diet_compat"]
cover = dc.groupby("supplement_id").diet_code.nunique()
for s_ in set(sup.supplement_id) - set(cover.index):
    W(f"{s_}: no diet compatibility rows (treat as unknown)")

if (dc[dc.compat_status.isin(["compatible", "incompatible"])].verification_status != "verified").any():
    E("supplement_diet_compat: compatible/incompatible must be verified")

# 8. Explanations
et = dfs["explanation_templates"]
allowed_crit = {"G", "D", "A", "L", "H", "SAFETY", "LIMIT"}
if sorted(set(et.criterion_code) - allowed_crit):
    E("explanation_templates: invalid criterion_code")
if (et.template_text.str.strip() == "").any():
    E("explanation_templates: empty template_text")

for claim_word in ["guarantee", "proven", "cure", "treat "]:
    if (
        et.template_text.str.lower().str.contains(claim_word).any()
        and not et.template_text.str.lower().str.contains("not guarantee").any()
    ):
        E(f"explanation_templates: contains clinical-claim wording '{claim_word}'")

# 9. Active goal mappings check
gm = dfs["supplement_goal_map"]
if not b(gm.is_active).any():
    W("no ACTIVE goal mappings: engine will return empty results until mappings are verified and activated")

# 10. Cross-directory consistency check if requested
if args.compare_dir:
    cmp_dir = args.compare_dir
    if not os.path.exists(cmp_dir):
        alt = os.path.join(os.path.dirname(os.path.abspath(__file__)), cmp_dir)
        if os.path.exists(alt):
            cmp_dir = alt
    if not os.path.exists(cmp_dir):
        E(f"Comparison directory '{cmp_dir}' not found.")
    else:
        cmp_sup_path = os.path.join(cmp_dir, "supplements.csv")
        if not os.path.exists(cmp_sup_path):
            E(f"Comparison directory '{cmp_dir}' missing supplements.csv")
        else:
            cmp_sup = pd.read_csv(cmp_sup_path, dtype=str, keep_default_na=False)
            if len(cmp_sup) != n_supps:
                E(f"Supplement count mismatch between '{D}' ({n_supps}) and '{cmp_dir}' ({len(cmp_sup)})")
            s1 = set(dfs["supplements"].supplement_id)
            s2 = set(cmp_sup.supplement_id)
            if s1 != s2:
                E(f"Supplement ID difference between datasets: {s1 ^ s2}")
            else:
                print(f"Verified synchronization with '{cmp_dir}': {len(s1)} identical supplement IDs.")

# Summary Output
n_ver = (dfs["supplements"].verification_status == "verified").sum()
n_rev = (dfs["supplements"].verification_status == "needs_review").sum()

print("=" * 60)
print(f"Knowledge Base Validation Summary for '{D}'")
print("=" * 60)
print(f"Total supplement records: {n_supps} (verified: {n_ver}, needs_review: {n_rev})")
print(f"Goal mappings:           {len(dfs['supplement_goal_map'])} (active: {b(dfs['supplement_goal_map'].is_active).sum()})")
print(f"Safety rules:            {len(dfs['safety_rules'])} (active: {b(dfs['safety_rules'].is_active).sum()})")
print(f"Diet compatibility:      {len(dfs['supplement_diet_compat'])}")
print(f"Allergen mappings:       {len(dfs['supplement_allergen'])}")
print(f"Activity mappings:       {len(dfs['supplement_activity_map'])}")
print(f"Lifestyle mappings:      {len(dfs['supplement_lifestyle_map'])}")
print(f"Files validated:         {len(dfs)} files")
print("-" * 60)

for w in warnings:
    print("WARNING:", w)
for e in errors:
    print("ERROR:", e)

print(f"\nResult: {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
