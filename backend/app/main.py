import os
import datetime as dt
import jwt
import bcrypt
import pandas as pd
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models import (
    Base, User, Profile, Run, RecommendationResult
)
from app.algorithms.engine import run as run_engine
from app.data_loader import load_kb

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_verified_path = os.path.join(_backend_dir, "data_verified")
_has_verified = os.path.isdir(_verified_path) or os.path.isdir("data_verified")
DEFAULT_DATA = "data_verified" if _has_verified else "data"
DATA = os.getenv("DATA_DIR", DEFAULT_DATA)

def get_data_dir() -> str:
    global DATA
    # Re-read environment variable if changed dynamically in tests
    current = os.getenv("DATA_DIR", DATA)
    if os.path.isabs(current) and os.path.isdir(current):
        return current
    if os.path.isdir(current):
        return current
    candidate = os.path.join(_backend_dir, current)
    if os.path.isdir(candidate):
        return candidate
    return current
SECRET = os.environ.get("JWT_SECRET", "super-secret-key-that-is-at-least-32-bytes-long")
engine_db = create_engine(os.getenv("DATABASE_URL", "sqlite:///./app.db"))
Session_ = sessionmaker(bind=engine_db)

# Create tables in database if not present
Base.metadata.create_all(engine_db)

app = FastAPI(
    title="Open Source Personalized Medicine & Supplement Recommendation Platform",
    description="Deterministic, rule-based supplement guidance platform (Group 101, B.Tech SRS v1.0).",
    version="1.0.0"
)

# Enable CORS for local Vite dev server and production clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer = HTTPBearer(auto_error=False)


def db():
    s = Session_()
    try:
        yield s
    finally:
        s.close()


def user(c=Depends(bearer), s: Session = Depends(db)) -> User:
    if not c or not c.credentials:
        raise HTTPException(401, "Authentication required")
    try:
        payload = jwt.decode(c.credentials, SECRET, algorithms=["HS256"])
        uid = payload["sub"]
    except Exception:
        raise HTTPException(401, "Invalid or expired session")
    u = s.get(User, int(uid))
    if not u:
        raise HTTPException(401, "Invalid session")
    return u


def token(u: User) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    exp = now + dt.timedelta(hours=8)
    return jwt.encode({"sub": str(u.id), "exp": exp, "iat": now}, SECRET, algorithm="HS256")


# Schemas
class Cred(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class ProfileIn(BaseModel):
    age: int = Field(ge=13, le=120)
    goals: List[str] = Field(min_length=1)
    dietary_preference: str
    allergies: List[str] = []
    existing_conditions: List[str] = []
    current_medication_classes: List[str] = []
    safety_confirmed: bool = False
    activity_level: str
    sleep_quality: str
    previous_usage: Dict[str, Dict[str, bool]] = Field(default_factory=dict)


def opts():
    data_dir = get_data_dir()
    r = lambda n: pd.read_csv(os.path.join(data_dir, f"{n}.csv"), dtype=str, keep_default_na=False, encoding="utf-8")
    supp_df = r("supplements")
    return {
        "goals": r("goals")[["goal_id", "goal_name"]].values.tolist(),
        "diets": r("diets").diet_code.tolist(),
        "allergens": r("allergens").allergen_code.tolist(),
        "conditions": r("conditions").condition_code.tolist(),
        "medication_classes": r("medication_classes").medclass_code.tolist(),
        "activity": r("activity_levels").activity_code.tolist(),
        "sleep": r("sleep_categories").sleep_code.tolist(),
        "supplements": supp_df[["supplement_id", "supplement_name"]].values.tolist()
    }


# Auth Endpoints
@app.post("/api/auth/register", status_code=201)
def register(c: Cred, s: Session = Depends(db)):
    if s.query(User).filter_by(email=c.email.lower()).first():
        raise HTTPException(409, "Email already registered")
    u = User(
        email=c.email.lower(),
        pw=bcrypt.hashpw(c.password.encode(), bcrypt.gensalt()).decode()
    )
    s.add(u)
    s.commit()
    return {"token": token(u)}


@app.post("/api/auth/login")
def login(c: Cred, s: Session = Depends(db)):
    u = s.query(User).filter_by(email=c.email.lower()).first()
    if not u or not bcrypt.checkpw(c.password.encode(), u.pw.encode()):
        raise HTTPException(401, "Invalid email or password")
    return {"token": token(u)}


@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully"}


@app.get("/api/auth/me")
def me(u: User = Depends(user)):
    return {"id": u.id, "email": u.email}


@app.get("/api/options")
def options():
    return opts()


@app.get("/api/system/mode")
def get_system_mode():
    data_dir = get_data_dir()
    is_verified = "data_verified" in data_dir
    return {
        "current_data_dir": data_dir,
        "is_verified": is_verified,
        "mode": "verified" if is_verified else "draft"
    }


@app.post("/api/system/mode")
def set_system_mode(body: dict):
    global DATA
    mode = body.get("mode", "verified")
    if mode == "verified":
        DATA = "data_verified"
    else:
        DATA = "data"
    os.environ["DATA_DIR"] = DATA
    data_dir = get_data_dir()
    return {
        "current_data_dir": data_dir,
        "is_verified": "data_verified" in data_dir,
        "mode": mode
    }


# Profile Endpoints
@app.get("/api/profile")
def get_profile(u: User = Depends(user), s: Session = Depends(db)):
    p = s.get(Profile, u.id)
    return p.data if p else None


@app.put("/api/profile")
def put_profile(b: ProfileIn, u: User = Depends(user), s: Session = Depends(db)):
    o = opts()
    d = b.model_dump()
    bad = (
        [g for g in d["goals"] if g not in [x[0] for x in o["goals"]]] +
        [a for a in d["allergies"] if a not in o["allergens"]] +
        [c for c in d["existing_conditions"] if c not in o["conditions"]] +
        [m for m in d["current_medication_classes"] if m not in o["medication_classes"]]
    )
    if (
        d["dietary_preference"] not in o["diets"] or
        d["activity_level"] not in o["activity"] or
        d["sleep_quality"] not in o["sleep"] or
        bad
    ):
        raise HTTPException(422, f"Invalid option(s): {bad or 'diet/activity/sleep'}")

    p = s.get(Profile, u.id)
    now = dt.datetime.now(dt.timezone.utc)
    if p:
        p.data = d
        p.updated_at = now
    else:
        p = Profile(user_id=u.id, data=d, updated_at=now)
        s.add(p)
    s.commit()
    return d


# Catalogue Endpoints
@app.get("/api/catalogue")
def catalogue(
    q: str = "",
    category: str = "",
    status: str = "",
    sort: str = "name_asc"
):
    data_dir = get_data_dir()
    kb = pd.read_csv(os.path.join(data_dir, "supplements.csv"), dtype=str, keep_default_na=False, encoding="utf-8")
    if q.strip():
        kb = kb[kb.supplement_name.str.contains(q, case=False, regex=False)]
    if category.strip():
        kb = kb[kb.supplement_category == category]
    if status.strip():
        kb = kb[kb.verification_status == status]

    if sort == "name_desc":
        kb = kb.sort_values("supplement_name", ascending=False)
    elif sort == "category":
        kb = kb.sort_values(["supplement_category", "supplement_name"])
    else:
        kb = kb.sort_values("supplement_name", ascending=True)

    cols = ["supplement_id", "supplement_name", "supplement_category", "verification_status", "source_url", "description", "active_ingredients", "ingredient_forms"]
    avail_cols = [c for c in cols if c in kb.columns]
    return kb[avail_cols].to_dict("records")


@app.get("/api/catalogue/{sid}")
def supplement(sid: str):
    data_dir = get_data_dir()
    r = lambda n: pd.read_csv(os.path.join(data_dir, f"{n}.csv"), dtype=str, keep_default_na=False, encoding="utf-8")
    sp = r("supplements")
    sp = sp[sp.supplement_id == sid]
    if sp.empty:
        raise HTTPException(404, "Supplement not found")

    f = lambda n: r(n)[lambda d: d.supplement_id == sid].to_dict("records")
    return {
        **sp.iloc[0].to_dict(),
        "goal_mappings": f("supplement_goal_map"),
        "diet_compat": f("supplement_diet_compat"),
        "safety_rules": f("safety_rules"),
        "allergens": f("supplement_allergen"),
        "note": "Absence of a recorded warning does not mean a supplement is safe. Unverified rows are candidates."
    }


# Recommendation Endpoints
@app.post("/api/recommendations", status_code=201)
def recommend(limit: Optional[int] = Query(5, ge=1, le=50), u: User = Depends(user), s: Session = Depends(db)):
    p = s.get(Profile, u.id)
    if not p:
        raise HTTPException(422, "Complete your health profile first")

    d = dict(p.data)
    if not d.pop("safety_confirmed", False):
        d["allergies"] = d["existing_conditions"] = d["current_medication_classes"] = None

    kb = load_kb(get_data_dir())
    res = run_engine(d, kb, limit=limit)

    names = {k: v["supplement_name"] for k, v in kb["supps"].items()}
    for k in ("excluded", "needs_review"):
        for x in res[k]:
            x["name"] = names.get(x["supplement_id"], x["supplement_id"])

    # Frozen snapshot persists profile state at the moment of recommendation
    now = dt.datetime.now(dt.timezone.utc)
    r = Run(
        user_id=u.id,
        created_at=now,
        status=res["status"],
        snapshot=p.data,
        result=res
    )
    s.add(r)
    s.flush()  # populate r.id

    # Persist individual candidate results for relational analysis
    for item in res.get("results", []):
        s.add(RecommendationResult(
            run_id=r.id,
            supplement_id=item["supplement_id"],
            eligibility_status="eligible",
            goal_match_score=float(item["values"].get("G", 0.0)),
            diet_match_score=float(item["values"].get("D", 0.0)),
            activity_match_score=float(item["values"].get("A", 0.0)),
            lifestyle_match_score=float(item["values"].get("L", 0.0)),
            history_match_score=float(item["values"].get("H", 0.0)),
            weighted_contributions=item.get("contributions"),
            final_score=float(item.get("score", 0.0)),
            rank_position=int(item.get("rank", 0)),
            explanation=item.get("explanation"),
            safety_summary=["Passed safety checks"],
            created_at=now
        ))
    for excl in res.get("excluded", []):
        s.add(RecommendationResult(
            run_id=r.id,
            supplement_id=excl["supplement_id"],
            eligibility_status="excluded_safety",
            safety_summary=[reason[1] for reason in excl.get("reasons", [])],
            created_at=now
        ))
    for rev in res.get("needs_review", []):
        s.add(RecommendationResult(
            run_id=r.id,
            supplement_id=rev["supplement_id"],
            eligibility_status="needs_review",
            safety_summary=[reason[1] for reason in rev.get("reasons", [])],
            created_at=now
        ))

    s.commit()
    return {"run_id": r.id, "created_at": r.created_at.isoformat(), **res}


@app.get("/api/recommendations")
def history(u: User = Depends(user), s: Session = Depends(db)):
    runs = s.query(Run).filter_by(user_id=u.id).order_by(Run.id.desc()).all()
    return [
        {
            "run_id": r.id,
            "created_at": r.created_at.isoformat() if r.created_at else "",
            "status": r.status,
            "n_results": len(r.result.get("results", [])),
            "rule_version": r.result.get("rule_version", ""),
            "scoring_version": r.result.get("scoring_version", "")
        }
        for r in runs
    ]


@app.get("/api/recommendations/{rid}")
def run_detail(rid: int, u: User = Depends(user), s: Session = Depends(db)):
    r = s.query(Run).filter_by(id=rid, user_id=u.id).first()
    if not r:
        raise HTTPException(404, "Run not found")
    return {
        "run_id": r.id,
        "created_at": r.created_at.isoformat() if r.created_at else "",
        "profile_snapshot": r.snapshot,
        **r.result
    }


# Static Frontend & SPA Fallback
frontend_dir = os.path.abspath(os.getenv("FRONTEND_DIR", os.path.join(os.path.dirname(__file__), "../../frontend/dist")))
if not os.path.isdir(frontend_dir):
    frontend_dir = os.path.abspath(os.getenv("FRONTEND_DIR", os.path.join(os.path.dirname(__file__), "../../frontend")))

if os.path.isdir(frontend_dir):
    index_html = os.path.join(frontend_dir, "index.html")
    assets_dir = os.path.join(frontend_dir, "assets")

    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(404, "Endpoint not found")
        target_file = os.path.join(frontend_dir, full_path)
        if os.path.isfile(target_file):
            return FileResponse(target_file)
        if os.path.isfile(index_html):
            return FileResponse(index_html)
        return {"status": "ok", "message": "Backend API online"}
