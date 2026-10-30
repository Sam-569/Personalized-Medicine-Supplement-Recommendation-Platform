"""SQLAlchemy ORM models for the Supplement Guidance Platform.
Fully compatible with PostgreSQL and SQLite.
"""
import datetime as dt
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    pw = Column(String(255), nullable=False)

    profiles = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    runs = relationship("Run", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "user_profiles"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    data = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))

    user = relationship("User", back_populates="profiles")


class Run(Base):
    __tablename__ = "recommendation_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))
    status = Column(String(50), nullable=False)
    snapshot = Column(JSON, nullable=False)
    result = Column(JSON, nullable=False)

    user = relationship("User", back_populates="runs")
    results = relationship("RecommendationResult", back_populates="run", cascade="all, delete-orphan")


class RecommendationResult(Base):
    __tablename__ = "recommendation_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, ForeignKey("recommendation_runs.id", ondelete="CASCADE"), index=True, nullable=False)
    supplement_id = Column(String(50), nullable=False)
    eligibility_status = Column(String(50), nullable=False)
    goal_match_score = Column(Float, nullable=True)
    diet_match_score = Column(Float, nullable=True)
    activity_match_score = Column(Float, nullable=True)
    lifestyle_match_score = Column(Float, nullable=True)
    history_match_score = Column(Float, nullable=True)
    weighted_contributions = Column(JSON, nullable=True)
    final_score = Column(Float, nullable=True)
    rank_position = Column(Integer, nullable=True)
    explanation = Column(JSON, nullable=True)
    safety_summary = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))

    run = relationship("Run", back_populates="results")


# --- Knowledge Base Tables ---

class Source(Base):
    __tablename__ = "sources"
    source_id = Column(String(50), primary_key=True)
    source_name = Column(String(255), nullable=False)
    source_type = Column(String(100))
    url = Column(Text)
    access_method = Column(Text)
    reuse_note = Column(Text)
    limitations = Column(Text)


class Goal(Base):
    __tablename__ = "goals"
    goal_id = Column(String(50), primary_key=True)
    goal_code = Column(String(100), unique=True, nullable=False)
    goal_name = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)


class Diet(Base):
    __tablename__ = "diets"
    diet_code = Column(String(50), primary_key=True)
    diet_name = Column(String(100), nullable=False)
    description = Column(Text)


class Allergen(Base):
    __tablename__ = "allergens"
    allergen_code = Column(String(50), primary_key=True)
    allergen_name = Column(String(100), nullable=False)


class Condition(Base):
    __tablename__ = "conditions"
    condition_code = Column(String(100), primary_key=True)
    condition_name = Column(String(255), nullable=False)
    in_scope_note = Column(Text)


class MedicationClass(Base):
    __tablename__ = "medication_classes"
    medclass_code = Column(String(100), primary_key=True)
    medclass_name = Column(String(255), nullable=False)
    note = Column(Text)


class ActivityLevel(Base):
    __tablename__ = "activity_levels"
    activity_code = Column(String(50), primary_key=True)
    activity_name = Column(String(100), nullable=False)
    ordinal = Column(Integer)


class SleepCategory(Base):
    __tablename__ = "sleep_categories"
    sleep_code = Column(String(50), primary_key=True)
    sleep_name = Column(String(100), nullable=False)
    ordinal = Column(Integer)


class Supplement(Base):
    __tablename__ = "supplements"
    supplement_id = Column(String(50), primary_key=True)
    supplement_name = Column(String(255), unique=True, nullable=False)
    supplement_category = Column(String(100), nullable=False)
    description = Column(Text)
    active_ingredients = Column(Text)
    ingredient_forms = Column(Text)
    primary_source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    source_url = Column(Text)
    verification_status = Column(String(50), nullable=False, default="needs_review")
    last_reviewed_at = Column(String(50))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(String(50))
    updated_at = Column(String(50))
    notes = Column(Text)


class SupplementGoalMap(Base):
    __tablename__ = "supplement_goal_map"
    mapping_id = Column(String(50), primary_key=True)
    supplement_id = Column(String(50), ForeignKey("supplements.supplement_id"), nullable=False)
    goal_id = Column(String(50), ForeignKey("goals.goal_id"), nullable=False)
    match_type = Column(String(50), nullable=False)
    match_score = Column(Float, nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    source_ref = Column(Text)
    evidence_notes = Column(Text)
    verification_status = Column(String(50), nullable=False)
    rule_version = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)


class SupplementActivityMap(Base):
    __tablename__ = "supplement_activity_map"
    map_id = Column(String(50), primary_key=True)
    supplement_id = Column(String(50), ForeignKey("supplements.supplement_id"), nullable=False)
    activity_code = Column(String(50), ForeignKey("activity_levels.activity_code"), nullable=False)
    match_type = Column(String(50), nullable=False)
    match_score = Column(Float, nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    source_ref = Column(Text)
    verification_status = Column(String(50), nullable=False)
    rule_version = Column(String(50))
    is_active = Column(Boolean, default=False, nullable=False)


class SupplementLifestyleMap(Base):
    __tablename__ = "supplement_lifestyle_map"
    map_id = Column(String(50), primary_key=True)
    supplement_id = Column(String(50), ForeignKey("supplements.supplement_id"), nullable=False)
    sleep_code = Column(String(50), ForeignKey("sleep_categories.sleep_code"), nullable=False)
    match_type = Column(String(50), nullable=False)
    match_score = Column(Float, nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    source_ref = Column(Text)
    verification_status = Column(String(50), nullable=False)
    rule_version = Column(String(50))
    is_active = Column(Boolean, default=False, nullable=False)


class SupplementDietCompat(Base):
    __tablename__ = "supplement_diet_compat"
    supplement_id = Column(String(50), ForeignKey("supplements.supplement_id"), primary_key=True)
    diet_code = Column(String(50), ForeignKey("diets.diet_code"), primary_key=True)
    compat_status = Column(String(50), nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    source_ref = Column(Text)
    verification_status = Column(String(50), nullable=False)
    last_reviewed_at = Column(String(50))
    notes = Column(Text)


class SupplementAllergen(Base):
    __tablename__ = "supplement_allergen"
    supplement_id = Column(String(50), ForeignKey("supplements.supplement_id"), primary_key=True)
    allergen_code = Column(String(50), ForeignKey("allergens.allergen_code"), primary_key=True)
    relation = Column(String(100))
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    source_ref = Column(Text)
    verification_status = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    notes = Column(Text)


class SafetyRule(Base):
    __tablename__ = "safety_rules"
    rule_id = Column(String(50), primary_key=True)
    supplement_id = Column(String(50), ForeignKey("supplements.supplement_id"), nullable=True)
    rule_type = Column(String(50), nullable=False)
    condition_code = Column(String(100), nullable=False)
    triggering_attribute = Column(String(100))
    action = Column(String(50), nullable=False)
    reason = Column(Text)
    safety_message = Column(Text, nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    source_ref = Column(Text)
    verification_status = Column(String(50), nullable=False)
    rule_version = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)


class ScoringConfig(Base):
    __tablename__ = "scoring_config"
    criterion_id = Column(String(50), primary_key=True)
    criterion_code = Column(String(50), unique=True, nullable=False)
    criterion_name = Column(String(100))
    weight = Column(Float, nullable=False)
    minimum_value = Column(Float, default=0.0, nullable=False)
    maximum_value = Column(Float, default=1.0, nullable=False)
    description = Column(Text)
    rule_version = Column(String(50))
    is_active = Column(Boolean, default=True, nullable=False)


class CriterionValueRule(Base):
    __tablename__ = "criterion_value_rules"
    rule_id = Column(String(50), primary_key=True)
    criterion_code = Column(String(50), ForeignKey("scoring_config.criterion_code"), nullable=False)
    condition = Column(Text)
    value = Column(Float, nullable=False)
    note = Column(Text)
    rule_version = Column(String(50))


class SystemConfig(Base):
    __tablename__ = "system_config"
    config_key = Column(String(100), primary_key=True)
    config_value = Column(String(255), nullable=False)
    description = Column(Text)
    rule_version = Column(String(50))


class ExplanationTemplate(Base):
    __tablename__ = "explanation_templates"
    template_id = Column(String(50), primary_key=True)
    criterion_code = Column(String(50), nullable=False)
    match_value = Column(String(50))
    template_text = Column(Text, nullable=False)
    required_attribute = Column(Text)
    rule_version = Column(String(50))
    is_active = Column(Boolean, default=True, nullable=False)

