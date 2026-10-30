"""Synthetic, clearly illustrative fixtures - NOT real clinical data."""
import copy, pytest
from app.algorithms import engine as E
from app.data_loader import load_kb

def kb():
    S = lambda n, v="verified": {"supplement_name": n, "verification_status": v}
    return {"supps": {"A": S("Alpha"), "B": S("Beta"), "C": S("Gamma"), "U": S("Unver", "needs_review")},
      "goal": {("A", "g1"): 1.0, ("B", "g1"): 1.0, ("C", "g1"): 0.5, ("U", "g1"): 1.0},
      "act": {}, "life": {}, "diet": {("A", "vegan"): "compatible", ("B", "vegan"): "incompatible", ("C", "vegan"): "compatible", ("U", "vegan"): "compatible"},
      "allergen": {("B", "fish")}, "rules": [{"rule_id": "RX", "supplement_id": "C", "condition_code": "cond1", "action": "require_review", "safety_message": "review"}],
      "weights": {"G": .4, "D": .2, "A": .15, "L": .15, "H": .1}, "threshold": 0.6,
      "dataset_version": "t", "rule_version": "t", "scoring_version": "t",
      "templates": [{"criterion_code": "G", "match_value": "1.0", "template_text": "Directly matches the selected goal."},
                    {"criterion_code": "LIMIT", "match_value": "all", "template_text": "Not medical advice."}]}
P = {"goals": ["g1"], "dietary_preference": "omnivore", "allergies": [], "existing_conditions": [],
     "current_medication_classes": [], "activity_level": "light", "sleep_quality": "good"}
ids = lambda r, k="results": [x["supplement_id"] for x in r[k]]

def test_unverified_never_scored():
    r = E.run(P, kb()); assert "U" not in ids(r) and "U" in ids(r, "needs_review")

def test_allergy_excluded_never_ranked():
    p = {**P, "allergies": ["fish"]}; r = E.run(p, kb())
    assert "B" in ids(r, "excluded") and "B" not in ids(r)

def test_diet_incompatible_excluded():
    r = E.run({**P, "dietary_preference": "vegan"}, kb()); assert "B" in ids(r, "excluded")

def test_unknown_diet_needs_review_not_safe():
    k = kb(); del k["diet"][("A", "vegan")]
    r = E.run({**P, "dietary_preference": "vegan"}, k); assert "A" in ids(r, "needs_review") and "A" not in ids(r)

def test_condition_rule_review():
    r = E.run({**P, "existing_conditions": ["cond1"]}, kb()); assert "C" in ids(r, "needs_review")

def test_incomplete_profile_withheld():
    r = E.run({**P, "current_medication_classes": None}, kb())
    assert r["status"] == "withheld_incomplete_profile" and r["results"] == []

def test_weights_sum_and_bounds():
    k = kb(); assert abs(sum(k["weights"].values()) - 1) < 1e-9
    assert all(0 <= x["score"] <= 1 for x in E.run(P, k)["results"])
    with pytest.raises(AssertionError): E.wsm({"G": 1}, {"G": .5})

def test_threshold_boundary():
    # partial goal(.5)*.4 + D 1*.2 + A .5*.15 + L .5*.15 + H .5*.1 = 0.60 exactly -> kept
    assert E.passes_threshold(0.6, 0.6) and E.passes_threshold(0.1 * 6, 0.6)
    assert not E.passes_threshold(0.599999, 0.6)

def test_tie_break_deterministic_and_repeatable():
    k = kb(); k["goal"][("B", "g1")] = 1.0
    r1, r2 = E.run(P, k), E.run(P, copy.deepcopy(k))
    assert r1 == r2 and ids(r1)[:2] == ["A", "B"]  # equal score+G -> supplement_id asc

def test_empty_results():
    k = kb(); k["goal"] = {}; r = E.run(P, k)
    assert r["status"] == "no_eligible_results" and r["results"] == []

def test_explanation_matches_breakdown():
    r = E.run(P, kb()); a = next(x for x in r["results"] if x["supplement_id"] == "A")
    assert "Directly matches the selected goal." in a["explanation"] and a["values"]["G"] == 1.0
    c = next(x for x in r["results"] if x["supplement_id"] == "C") if any(x["supplement_id"] == "C" for x in r["results"]) else None
    assert c is None or "Directly matches the selected goal." not in c["explanation"]

def test_real_dataset_withholds_until_verified():
    r = E.run({**P, "goals": ["GL01"]}, load_kb("data"))
    assert r["results"] == [] and len(r["needs_review"]) == 130
