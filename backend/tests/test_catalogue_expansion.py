"""Comprehensive tests for the expanded supplement dataset,
recommendation algorithm, safety filter, WSM scoring, and catalogue endpoints.
"""
import os
import sys
import copy
import pytest
import pandas as pd

# Add dataset folder to sys.path
dataset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "dataset")
if dataset_dir not in sys.path:
    sys.path.insert(0, dataset_dir)

from fastapi.testclient import TestClient

from app.main import app
from app.algorithms import engine as E
from app.data_loader import load_kb
from app.data_importer import validate_and_import
import supplement_data as sd

client = TestClient(app)

AUTH_HEADER = None


@pytest.fixture(autouse=True)
def setup_auth_fixture():
    global AUTH_HEADER
    email = f"eval_{os.urandom(4).hex()}@example.com"
    r = client.post("/api/auth/register", json={"email": email, "password": "securepassword123"})
    token = r.json()["token"]
    AUTH_HEADER = {"Authorization": f"Bearer {token}"}


def test_catalogue_has_at_least_100_distinct_supplements():
    """Requirement 1: Dataset contains at least 100 distinct supplement records."""
    kb_verified = load_kb("data_verified")
    kb_draft = load_kb("data")
    assert len(kb_verified["supps"]) >= 100
    assert len(kb_draft["supps"]) >= 100
    assert len(kb_verified["supps"]) == 130
    assert len(kb_draft["supps"]) == 130


def test_existing_ids_preserved_and_no_duplicates():
    """Requirements 3 & 4: Existing supplement IDs remain unchanged and no duplicate IDs or names."""
    kb = load_kb("data_verified")
    supps = kb["supps"]

    # Verify original 24 IDs and exact names
    original_24 = {
        "SUP001": "Vitamin D", "SUP002": "Vitamin B12", "SUP003": "Vitamin B6",
        "SUP004": "Vitamin C", "SUP005": "Vitamin E", "SUP006": "Vitamin K",
        "SUP007": "Vitamin A", "SUP008": "Folate", "SUP009": "Biotin",
        "SUP010": "Choline", "SUP011": "Calcium", "SUP012": "Iron",
        "SUP013": "Magnesium", "SUP014": "Zinc", "SUP015": "Selenium",
        "SUP016": "Iodine", "SUP017": "Potassium", "SUP018": "Omega-3 fatty acids",
        "SUP019": "Probiotics", "SUP020": "Melatonin", "SUP021": "Ashwagandha",
        "SUP022": "Turmeric / curcumin", "SUP023": "Ginkgo", "SUP024": "Creatine"
    }

    for sid, name in original_24.items():
        assert sid in supps, f"Missing foundational ID: {sid}"
        assert supps[sid]["supplement_name"] == name, f"Name mismatch for {sid}"

    # Verify no duplicates
    names = [s["supplement_name"].lower() for s in supps.values()]
    assert len(names) == len(set(names)), "Duplicate supplement names detected"
    ids = list(supps.keys())
    assert len(ids) == len(set(ids)), "Duplicate supplement IDs detected"


def test_balanced_category_representation():
    """Requirement 2: Balanced distribution across required nutritional categories."""
    kb = load_kb("data_verified")
    categories = {}
    for s in kb["supps"].values():
        cat = s["supplement_category"]
        categories[cat] = categories.get(cat, 0) + 1

    expected_categories = [
        "vitamin", "mineral", "fatty_acid", "protein_amino_acid",
        "amino_acid_derivative", "electrolyte", "fiber_prebiotic",
        "probiotic", "botanical", "nutrient", "hormone_supplement"
    ]
    for cat in expected_categories:
        assert cat in categories, f"Missing category: {cat}"
        assert categories[cat] >= 1, f"Empty category: {cat}"


def test_foreign_key_references_integrity():
    """Requirement 5: All related mappings reference valid IDs."""
    kb = load_kb("data_verified")
    supp_ids = set(kb["supps"].keys())

    for (sid, gid) in kb["goal"].keys():
        assert sid in supp_ids, f"Goal map references unknown supplement: {sid}"
    for (sid, act) in kb["act"].keys():
        assert sid in supp_ids, f"Activity map references unknown supplement: {sid}"
    for (sid, sleep) in kb["life"].keys():
        assert sid in supp_ids, f"Lifestyle map references unknown supplement: {sid}"
    for (sid, diet) in kb["diet"].keys():
        assert sid in supp_ids, f"Diet compat references unknown supplement: {sid}"
    for (sid, allergen) in kb["allergen"]:
        assert sid in supp_ids, f"Allergen map references unknown supplement: {sid}"
    for rule in kb["rules"]:
        assert rule["supplement_id"] in ("", *supp_ids), f"Rule references unknown supplement: {rule['supplement_id']}"


def test_unverified_supplements_never_eligible():
    """Requirement 10: Unverified supplements cannot enter eligible recommendations."""
    kb = load_kb("data_verified")

    # Pick an unverified candidate supplement (e.g., SUP029 Vitamin B-Complex)
    unverified_id = "SUP029"
    assert kb["supps"][unverified_id]["verification_status"] != "verified"

    profile = {
        "goals": ["GL02"], "dietary_preference": "omnivore",
        "allergies": [], "existing_conditions": [], "current_medication_classes": [],
        "activity_level": "moderate", "sleep_quality": "good"
    }

    res = E.run(profile, kb)
    eligible_ids = [r["supplement_id"] for r in res["results"]]
    review_ids = [r["supplement_id"] for r in res["needs_review"]]

    assert unverified_id not in eligible_ids
    assert unverified_id in review_ids

    # Verify R000 reason is explicitly attached
    rev_entry = next(r for r in res["needs_review"] if r["supplement_id"] == unverified_id)
    assert any(reason[0] == "R000" for reason in rev_entry["reasons"])


def test_hard_safety_exclusion_overrides_high_score():
    """Requirement 11: Safety exclusion rules strictly override any goal match score."""
    kb = load_kb("data_verified")

    # User with kidney disease: Potassium (SUP017) and Potassium Citrate (SUP077) must be excluded
    profile = {
        "goals": ["GL05"], "dietary_preference": "omnivore",
        "allergies": [], "existing_conditions": ["kidney_disease"],
        "current_medication_classes": [],
        "activity_level": "moderate", "sleep_quality": "good"
    }

    res = E.run(profile, kb)
    eligible_ids = [r["supplement_id"] for r in res["results"]]
    excluded_ids = [r["supplement_id"] for r in res["excluded"]]

    assert "SUP017" in excluded_ids
    assert "SUP017" not in eligible_ids
    assert "SUP077" in excluded_ids
    assert "SUP077" not in eligible_ids


def test_allergy_exclusion_overrides_score():
    """Requirement 11: Declared allergen permanently disqualifies candidate supplement."""
    kb = load_kb("data_verified")

    # User allergic to milk: Whey protein isolate (SUP053) must be excluded
    profile = {
        "goals": ["GL07"], "dietary_preference": "omnivore",
        "allergies": ["milk"], "existing_conditions": [],
        "current_medication_classes": [],
        "activity_level": "high", "sleep_quality": "good"
    }

    res = E.run(profile, kb)
    eligible_ids = [r["supplement_id"] for r in res["results"]]
    excluded_ids = [r["supplement_id"] for r in res["excluded"]]

    assert "SUP053" in excluded_ids
    assert "SUP053" not in eligible_ids


def test_vegan_dietary_preference_excludes_animal_sources():
    """Requirement 11: Incompatible dietary preference excludes animal-based supplements."""
    kb = load_kb("data_verified")

    # User on vegan diet: Cod liver oil (SUP044) and Whey (SUP053) must be excluded
    profile = {
        "goals": ["GL05", "GL07"], "dietary_preference": "vegan",
        "allergies": [], "existing_conditions": [],
        "current_medication_classes": [],
        "activity_level": "high", "sleep_quality": "good"
    }

    res = E.run(profile, kb)
    eligible_ids = [r["supplement_id"] for r in res["results"]]
    excluded_ids = [r["supplement_id"] for r in res["excluded"]]

    assert "SUP053" in excluded_ids
    assert "SUP053" not in eligible_ids


def test_wsm_weights_formula_and_threshold_enforcement():
    """Requirements 13 & 14: WSM scoring formula S = 0.40G + 0.20D + 0.15A + 0.15L + 0.10H and 0.60 threshold."""
    kb = load_kb("data_verified")

    weights = kb["weights"]
    assert abs(weights["G"] - 0.40) < 1e-9
    assert abs(weights["D"] - 0.20) < 1e-9
    assert abs(weights["A"] - 0.15) < 1e-9
    assert abs(weights["L"] - 0.15) < 1e-9
    assert abs(weights["H"] - 0.10) < 1e-9
    assert abs(sum(weights.values()) - 1.0) < 1e-9
    assert abs(kb["threshold"] - 0.60) < 1e-9

    # Test calculation
    vals = {"G": 1.0, "D": 1.0, "A": 0.5, "L": 0.5, "H": 0.5}
    expected_score = 0.40*1.0 + 0.20*1.0 + 0.15*0.5 + 0.15*0.5 + 0.10*0.5  # 0.80
    calculated = E.wsm(vals, weights)
    assert abs(calculated - expected_score) < 1e-9
    assert E.passes_threshold(calculated, 0.60)

    # Sub-threshold: G=0.0 -> score = 0.40
    vals_low = {"G": 0.0, "D": 1.0, "A": 0.5, "L": 0.5, "H": 0.5}
    assert not E.passes_threshold(E.wsm(vals_low, weights), 0.60)


def test_deterministic_ranking_and_tie_breaking():
    """Requirement 15: Ranking is completely deterministic with tie breakers (score desc, G desc, id asc)."""
    kb = load_kb("data_verified")

    profile = {
        "goals": ["GL01"], "dietary_preference": "omnivore",
        "allergies": [], "existing_conditions": [], "current_medication_classes": [],
        "activity_level": "moderate", "sleep_quality": "good"
    }

    run1 = E.run(profile, kb)
    run2 = E.run(profile, copy.deepcopy(kb))

    assert run1["results"] == run2["results"]
    for i, res in enumerate(run1["results"], 1):
        assert res["rank"] == i


def test_catalogue_api_category_filter_and_sorting():
    """Requirement 9: Catalogue endpoint supports filtering and sorting over the 130 records."""
    # Filter by category
    r = client.get("/api/catalogue?category=botanical")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 20
    assert all(item["supplement_category"] == "botanical" for item in items)

    # Filter by status
    r_ver = client.get("/api/catalogue?status=verified")
    assert r_ver.status_code == 200
    assert all(item["verification_status"] == "verified" for item in r_ver.json())

    r_rev = client.get("/api/catalogue?status=needs_review")
    assert r_rev.status_code == 200
    assert all(item["verification_status"] == "needs_review" for item in r_rev.json())

    # Sort descending
    r_sort = client.get("/api/catalogue?sort=name_desc")
    assert r_sort.status_code == 200
    names = [item["supplement_name"] for item in r_sort.json()]
    assert names == sorted(names, reverse=True)
