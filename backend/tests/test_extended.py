"""Extended tests verifying safety exclusion enforcement, WSM calculations,
previous usage criterion, catalogue search, and dataset importer repeatability.
"""
import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app, Session_, engine_db
from app.models import Base, RecommendationResult
from app.algorithms import engine as E
from app.data_loader import load_kb
from app.data_importer import validate_and_import

client = TestClient(app)

AUTH_HEADER = None


@pytest.fixture(autouse=True)
def setup_auth():
    global AUTH_HEADER
    email = f"test_{os.urandom(4).hex()}@example.com"
    r = client.post("/api/auth/register", json={"email": email, "password": "securepassword123"})
    token = r.json()["token"]
    AUTH_HEADER = {"Authorization": f"Bearer {token}"}


def test_previous_usage_scoring_and_reaction():
    """Verify Criterion H values: 0.5 (never used), 1.0 (used without reaction), 0.0 (used with reaction)."""
    kb_data = {
        "supps": {"A": {"supplement_name": "Alpha", "verification_status": "verified"}},
        "goal": {("A", "g1"): 1.0},
        "act": {}, "life": {}, "diet": {("A", "omnivore"): "compatible"},
        "allergen": set(), "rules": [],
        "weights": {"G": 0.4, "D": 0.2, "A": 0.15, "L": 0.15, "H": 0.1},
        "threshold": 0.60,
        "dataset_version": "v1", "rule_version": "v1", "scoring_version": "v1",
        "templates": [{"criterion_code": "LIMIT", "match_value": "all", "template_text": "Medical disclaimer."}]
    }

    # Case 1: Never used -> H = 0.5
    p1 = {"goals": ["g1"], "dietary_preference": "omnivore", "allergies": [], "existing_conditions": [], "current_medication_classes": [], "activity_level": "light", "sleep_quality": "good", "previous_usage": {}}
    v1 = E.criterion_values("A", p1, kb_data)
    assert v1["H"] == 0.5

    # Case 2: Used with no reaction -> H = 1.0
    p2 = {**p1, "previous_usage": {"A": {"used": True, "reaction": False}}}
    v2 = E.criterion_values("A", p2, kb_data)
    assert v2["H"] == 1.0

    # Case 3: Used with reaction -> H = 0.0 and safety review triggered
    p3 = {**p1, "previous_usage": {"A": {"used": True, "reaction": True}}}
    v3 = E.criterion_values("A", p3, kb_data)
    assert v3["H"] == 0.0
    status, reasons = E.safety_check("A", p3, kb_data)
    assert status == "needs_review"
    assert any("prior reaction" in r[1].lower() for r in reasons)


def test_safety_excluded_never_in_final_results():
    """A safety-excluded supplement must NEVER appear in final results, regardless of high score."""
    kb_data = {
        "supps": {
            "S_EXCL": {"supplement_name": "DangerHerb", "verification_status": "verified"},
            "S_SAFE": {"supplement_name": "SafeMineral", "verification_status": "verified"}
        },
        "goal": {("S_EXCL", "g1"): 1.0, ("S_SAFE", "g1"): 1.0},
        "act": {("S_EXCL", "high"): 1.0, ("S_SAFE", "high"): 1.0},
        "life": {("S_EXCL", "good"): 1.0, ("S_SAFE", "good"): 1.0},
        "diet": {("S_EXCL", "omnivore"): "compatible", ("S_SAFE", "omnivore"): "compatible"},
        "allergen": {("S_EXCL", "peanut")},  # peanut allergen
        "rules": [],
        "weights": {"G": 0.4, "D": 0.2, "A": 0.15, "L": 0.15, "H": 0.1},
        "threshold": 0.60,
        "dataset_version": "v1", "rule_version": "v1", "scoring_version": "v1",
        "templates": [{"criterion_code": "LIMIT", "match_value": "all", "template_text": "Medical disclaimer."}]
    }

    # User allergic to peanut
    profile = {
        "goals": ["g1"], "dietary_preference": "omnivore",
        "allergies": ["peanut"], "existing_conditions": [], "current_medication_classes": [],
        "activity_level": "high", "sleep_quality": "good"
    }

    res = E.run(profile, kb_data)
    result_ids = [r["supplement_id"] for r in res["results"]]
    excluded_ids = [e["supplement_id"] for e in res["excluded"]]

    assert "S_EXCL" not in result_ids
    assert "S_EXCL" in excluded_ids
    assert "S_SAFE" in result_ids


def test_catalogue_search_filter_and_detail():
    """Verify catalogue search by query and detail view with safety disclaimer."""
    # Search for vitamin
    r = client.get("/api/catalogue?q=Vitamin")
    assert r.status_code == 200
    items = r.json()
    assert len(items) > 0
    assert all("vitamin" in item["supplement_name"].lower() for item in items)

    # Detail view
    first_id = items[0]["supplement_id"]
    r_detail = client.get(f"/api/catalogue/{first_id}")
    assert r_detail.status_code == 200
    detail = r_detail.json()
    assert "note" in detail
    assert "Absence of a recorded warning does not mean a supplement is safe" in detail["note"]
    assert "goal_mappings" in detail
    assert "safety_rules" in detail


def test_options_contains_controlled_vocabularies():
    """Verify /api/options returns goals, diets, allergens, conditions, medication_classes, activity, sleep."""
    r = client.get("/api/options")
    assert r.status_code == 200
    data = r.json()
    for key in ("goals", "diets", "allergens", "conditions", "medication_classes", "activity", "sleep", "supplements"):
        assert key in data
        assert len(data[key]) > 0


def test_data_importer_idempotency_on_isolated_db():
    """Verify validate_and_import is repeatable and prevents duplicate insertions."""
    temp_dir = tempfile.mkdtemp()
    temp_db_path = os.path.join(temp_dir, "test_isolated.db")
    test_engine = create_engine(f"sqlite:///{temp_db_path}")
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine)

    session = TestSession()
    try:
        # First import
        res1 = validate_and_import("data", session)
        assert len(res1["errors"]) == 0
        assert res1["imported"]["supplements"] == 130

        # Second import (repeatable)
        res2 = validate_and_import("data", session)
        assert len(res2["errors"]) == 0
        assert res2["imported"]["supplements"] == 0
        assert res2["skipped"]["supplements"] == 130
    finally:
        session.close()


def test_recommendation_results_persisted_to_relational_table():
    """Verify recommendation results are saved both in Run.result and RecommendationResult table."""
    # Complete profile
    p_data = {
        "age": 28, "goals": ["GL01"], "dietary_preference": "omnivore",
        "allergies": [], "existing_conditions": [], "current_medication_classes": [],
        "safety_confirmed": True, "activity_level": "moderate", "sleep_quality": "good",
        "previous_usage": {}
    }
    client.put("/api/profile", json=p_data, headers=AUTH_HEADER)

    # Generate recommendation
    r = client.post("/api/recommendations", headers=AUTH_HEADER)
    assert r.status_code == 201
    run_id = r.json()["run_id"]

    # Verify rows in recommendation_results table
    s = Session_()
    try:
        saved_items = s.query(RecommendationResult).filter_by(run_id=run_id).all()
        assert len(saved_items) > 0
        assert all(item.run_id == run_id for item in saved_items)
    finally:
        s.close()


def test_top_n_recommendation_threshold_cutoff():
    """Verify that when multiple supplements exceed the cutoff score threshold,
    the recommendation engine limits output to top 5 by default, or top 6 when requested."""
    kb_data = load_kb("data_verified")
    multi_goal_profile = {
        "goals": ["GL01", "GL02", "GL03", "GL04", "GL05"],
        "dietary_preference": "omnivore",
        "allergies": [],
        "existing_conditions": [],
        "current_medication_classes": [],
        "activity_level": "moderate",
        "sleep_quality": "good",
        "previous_usage": {}
    }

    # Default limit = 5
    res_default = E.run(multi_goal_profile, kb_data)
    assert res_default["total_eligible"] > 5
    assert len(res_default["results"]) == 5
    assert [r["rank"] for r in res_default["results"]] == [1, 2, 3, 4, 5]

    # Explicit limit = 6
    res_6 = E.run(multi_goal_profile, kb_data, limit=6)
    assert len(res_6["results"]) == 6
    assert [r["rank"] for r in res_6["results"]] == [1, 2, 3, 4, 5, 6]

    # API endpoint with default limit=5
    old_env = os.environ.get("DATA_DIR")
    try:
        os.environ["DATA_DIR"] = "data_verified"
        client.put("/api/profile", json={**multi_goal_profile, "age": 25, "safety_confirmed": True}, headers=AUTH_HEADER)
        # Default API endpoint always gives top 5
        r_default = client.post("/api/recommendations", headers=AUTH_HEADER)
        assert r_default.status_code == 201
        assert len(r_default.json()["results"]) == 5
        assert r_default.json()["limit"] == 5
    finally:
        if old_env is not None:
            os.environ["DATA_DIR"] = old_env
        else:
            os.environ.pop("DATA_DIR", None)





