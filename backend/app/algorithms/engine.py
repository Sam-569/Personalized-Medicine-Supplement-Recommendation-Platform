"""Deterministic recommendation engine (no ML/AI). Pipeline:
validate -> safety filter -> goal match -> WSM -> threshold -> rank -> explain.
Pure functions over an in-memory knowledge base (see app/data_loader.py)."""
from decimal import Decimal

TOL = 1e-9
REQUIRED = ["goals", "dietary_preference", "allergies", "existing_conditions",
            "current_medication_classes", "activity_level", "sleep_quality"]

def validate_profile(p):
    """None = unanswered (blocks safety checks); [] = answered 'none'."""
    return [f for f in REQUIRED if p.get(f) in (None, "") or (f == "goals" and not p.get(f))]

def safety_check(sid, p, kb):
    """Returns (status, reasons) status in eligible|excluded|needs_review. Unknown is never safe."""
    ex, rv = [], []
    s = kb["supps"][sid]
    if s["verification_status"] != "verified":
        rv.append(("R000", "Safety information not verified for this supplement."))
    if p["dietary_preference"] != "omnivore":
        c = kb["diet"].get((sid, p["dietary_preference"]), "unknown")
        if c == "incompatible": ex.append(("DIET", "Incompatible with recorded dietary preference."))
        elif c != "compatible": rv.append(("DIET", "Dietary compatibility unknown or product-dependent."))
    for a in p["allergies"]:
        if (sid, a) in kb["allergen"]: ex.append(("ALLERGY", f"Allergen conflict: {a}."))
    triggers = set(p["existing_conditions"]) | set(p["current_medication_classes"])
    for r in kb["rules"]:
        if r["supplement_id"] in ("", sid) and r["condition_code"] in triggers:
            (ex if r["action"] == "exclude" else rv).append((r["rule_id"], r["safety_message"]))
    if p.get("previous_usage", {}).get(sid, {}).get("reaction"):
        rv.append(("REACTION", "You reported a prior reaction to this supplement."))
    if ex: return "excluded", ex
    if rv: return "needs_review", rv
    return "eligible", []

def criterion_values(sid, p, kb):
    g = max([kb["goal"].get((sid, x), 0.0) for x in p["goals"]] or [0.0])
    d = 1.0 if p["dietary_preference"] == "omnivore" or kb["diet"].get((sid, p["dietary_preference"])) == "compatible" else 0.0
    a = kb["act"].get((sid, p["activity_level"]), 0.0)
    l = kb["life"].get((sid, p["sleep_quality"]), 0.0)
    u = p.get("previous_usage", {}).get(sid)
    h = 0.5 if not u or not u.get("used") else (0.0 if u.get("reaction") else 1.0)
    return {"G": g, "D": d, "A": a, "L": l, "H": h}

def wsm(vals, weights):
    assert abs(sum(weights.values()) - 1.0) <= TOL, "weights must sum to 1.0"
    return sum(weights[k] * vals[k] for k in weights)

def passes_threshold(score, t):
    return Decimal(str(round(score, 9))) >= Decimal(str(t))

def explain(vals, kb):
    out = [t["template_text"] for t in kb["templates"]
           if t["criterion_code"] in vals and float(t["match_value"] or -1) == vals[t["criterion_code"]]
           and t["criterion_code"] != "H"]
    out += [t["template_text"] for t in kb["templates"] if t["criterion_code"] in ("SAFETY",) and t["match_value"] == "pass"]
    return out + [t["template_text"] for t in kb["templates"] if t["criterion_code"] == "LIMIT"]

def run(p, kb, limit=None):
    missing = validate_profile(p)
    max_rec = limit if limit is not None else kb.get("max_recommendations", 5)
    meta = {k: kb[k] for k in ("dataset_version", "rule_version", "scoring_version", "threshold")} | {
        "weights": kb["weights"],
        "max_recommendations": max_rec
    }
    if missing:
        return {"status": "withheld_incomplete_profile", "missing_fields": missing, "results": [], "total_eligible": 0, "excluded": [], "needs_review": [], **meta}
    elig, excluded, review = [], [], []
    for sid in sorted(kb["supps"]):
        st, why = safety_check(sid, p, kb)
        if st == "excluded": excluded.append({"supplement_id": sid, "reasons": why})
        elif st == "needs_review": review.append({"supplement_id": sid, "reasons": why})
        else: elig.append(sid)
    scored = []
    for sid in elig:                       # only safety-eligible reach scoring
        v = criterion_values(sid, p, kb)
        s = wsm(v, kb["weights"])
        scored.append({"supplement_id": sid, "values": v, "contributions": {k: kb["weights"][k] * v[k] for k in v}, "score": round(s, 6)})
    all_kept = [x for x in scored if passes_threshold(x["score"], kb["threshold"])]
    all_kept.sort(key=lambda x: (-x["score"], -x["values"]["G"], x["supplement_id"]))
    total_eligible = len(all_kept)

    # Threshold capping: Retain top N recommendations (default 5 or user specified)
    if max_rec is not None and max_rec > 0:
        kept = all_kept[:max_rec]
    else:
        kept = all_kept

    for i, x in enumerate(kept, 1):
        x["rank"] = i; x["name"] = kb["supps"][x["supplement_id"]]["supplement_name"]; x["explanation"] = explain(x["values"], kb)
    status = "completed" if kept else "no_eligible_results"
    return {
        "status": status,
        "results": kept,
        "total_eligible": total_eligible,
        "limit": max_rec,
        "excluded": excluded,
        "needs_review": review,
        **meta
    }

