import os, tempfile
os.environ["DATA_DIR"] = "data"
os.environ["JWT_SECRET"] = "test-secret-that-is-at-least-32-characters-long"; os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/t.db"; os.environ["FRONTEND_DIR"] = "."
from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)
PROFILE = {"age": 30, "goals": ["GL01"], "dietary_preference": "omnivore", "allergies": [], "existing_conditions": [], "current_medication_classes": [],
           "safety_confirmed": True, "activity_level": "light", "sleep_quality": "good"}
def auth(email):
    t = c.post("/api/auth/register", json={"email": email, "password": "password123"}).json()["token"]; return {"Authorization": f"Bearer {t}"}
def test_auth_and_duplicates():
    auth("a@x.com"); assert c.post("/api/auth/register", json={"email": "a@x.com", "password": "password123"}).status_code == 409
    assert c.post("/api/auth/login", json={"email": "a@x.com", "password": "wrongpass1"}).status_code == 401
    assert c.get("/api/profile").status_code == 401
def test_profile_validation():
    h = auth("b@x.com"); assert c.put("/api/profile", json={**PROFILE, "goals": ["bogus"]}, headers=h).status_code == 422
    assert c.put("/api/profile", json={**PROFILE, "goals": []}, headers=h).status_code == 422
def test_recommend_requires_profile_and_withholds_unverified():
    h = auth("c@x.com"); assert c.post("/api/recommendations", headers=h).status_code == 422
    c.put("/api/profile", json=PROFILE, headers=h); r = c.post("/api/recommendations", headers=h).json()
    assert r["status"] == "no_eligible_results" and r["results"] == [] and len(r["needs_review"]) == 130
def test_unconfirmed_safety_withholds():
    h = auth("d@x.com"); c.put("/api/profile", json={**PROFILE, "safety_confirmed": False}, headers=h)
    assert c.post("/api/recommendations", headers=h).json()["status"] == "withheld_incomplete_profile"
def test_history_ownership_and_freeze():
    h1, h2 = auth("e@x.com"), auth("f@x.com"); c.put("/api/profile", json=PROFILE, headers=h1)
    rid = c.post("/api/recommendations", headers=h1).json()["run_id"]
    c.put("/api/profile", json={**PROFILE, "goals": ["GL02"]}, headers=h1)
    assert c.get(f"/api/recommendations/{rid}", headers=h1).json()["profile_snapshot"]["goals"] == ["GL01"]
    assert c.get(f"/api/recommendations/{rid}", headers=h2).status_code == 404
    assert c.get("/api/recommendations", headers=h2).json() == []
