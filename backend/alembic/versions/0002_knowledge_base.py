"""Knowledge base and recommendation results tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-10
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    # Recommendation results per run
    op.create_table(
        'recommendation_results',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('run_id', sa.Integer(), sa.ForeignKey('recommendation_runs.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('supplement_id', sa.String(50), nullable=False),
        sa.Column('eligibility_status', sa.String(50), nullable=False),
        sa.Column('goal_match_score', sa.Float(), nullable=True),
        sa.Column('diet_match_score', sa.Float(), nullable=True),
        sa.Column('activity_match_score', sa.Float(), nullable=True),
        sa.Column('lifestyle_match_score', sa.Float(), nullable=True),
        sa.Column('history_match_score', sa.Float(), nullable=True),
        sa.Column('weighted_contributions', sa.JSON(), nullable=True),
        sa.Column('final_score', sa.Float(), nullable=True),
        sa.Column('rank_position', sa.Integer(), nullable=True),
        sa.Column('explanation', sa.JSON(), nullable=True),
        sa.Column('safety_summary', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    # Knowledge base reference tables
    op.create_table(
        'sources',
        sa.Column('source_id', sa.String(50), primary_key=True),
        sa.Column('source_name', sa.String(255), nullable=False),
        sa.Column('source_type', sa.String(100), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('access_method', sa.Text(), nullable=True),
        sa.Column('reuse_note', sa.Text(), nullable=True),
        sa.Column('limitations', sa.Text(), nullable=True)
    )

    op.create_table(
        'goals',
        sa.Column('goal_id', sa.String(50), primary_key=True),
        sa.Column('goal_code', sa.String(100), unique=True, nullable=False),
        sa.Column('goal_name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False)
    )

    op.create_table(
        'diets',
        sa.Column('diet_code', sa.String(50), primary_key=True),
        sa.Column('diet_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True)
    )

    op.create_table(
        'allergens',
        sa.Column('allergen_code', sa.String(50), primary_key=True),
        sa.Column('allergen_name', sa.String(100), nullable=False)
    )

    op.create_table(
        'conditions',
        sa.Column('condition_code', sa.String(100), primary_key=True),
        sa.Column('condition_name', sa.String(255), nullable=False),
        sa.Column('in_scope_note', sa.Text(), nullable=True)
    )

    op.create_table(
        'medication_classes',
        sa.Column('medclass_code', sa.String(100), primary_key=True),
        sa.Column('medclass_name', sa.String(255), nullable=False),
        sa.Column('note', sa.Text(), nullable=True)
    )

    op.create_table(
        'activity_levels',
        sa.Column('activity_code', sa.String(50), primary_key=True),
        sa.Column('activity_name', sa.String(100), nullable=False),
        sa.Column('ordinal', sa.Integer(), nullable=True)
    )

    op.create_table(
        'sleep_categories',
        sa.Column('sleep_code', sa.String(50), primary_key=True),
        sa.Column('sleep_name', sa.String(100), nullable=False),
        sa.Column('ordinal', sa.Integer(), nullable=True)
    )

    op.create_table(
        'supplements',
        sa.Column('supplement_id', sa.String(50), primary_key=True),
        sa.Column('supplement_name', sa.String(255), unique=True, nullable=False),
        sa.Column('supplement_category', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('active_ingredients', sa.Text(), nullable=True),
        sa.Column('ingredient_forms', sa.Text(), nullable=True),
        sa.Column('primary_source_id', sa.String(50), sa.ForeignKey('sources.source_id'), nullable=True),
        sa.Column('source_url', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), default='needs_review', nullable=False),
        sa.Column('last_reviewed_at', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.String(50), nullable=True),
        sa.Column('updated_at', sa.String(50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True)
    )

    op.create_table(
        'supplement_goal_map',
        sa.Column('mapping_id', sa.String(50), primary_key=True),
        sa.Column('supplement_id', sa.String(50), sa.ForeignKey('supplements.supplement_id'), nullable=False),
        sa.Column('goal_id', sa.String(50), sa.ForeignKey('goals.goal_id'), nullable=False),
        sa.Column('match_type', sa.String(50), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False),
        sa.Column('source_id', sa.String(50), sa.ForeignKey('sources.source_id'), nullable=True),
        sa.Column('source_ref', sa.Text(), nullable=True),
        sa.Column('evidence_notes', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), nullable=False),
        sa.Column('rule_version', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=False, nullable=False)
    )

    op.create_table(
        'supplement_activity_map',
        sa.Column('map_id', sa.String(50), primary_key=True),
        sa.Column('supplement_id', sa.String(50), sa.ForeignKey('supplements.supplement_id'), nullable=False),
        sa.Column('activity_code', sa.String(50), sa.ForeignKey('activity_levels.activity_code'), nullable=False),
        sa.Column('match_type', sa.String(50), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False),
        sa.Column('source_id', sa.String(50), sa.ForeignKey('sources.source_id'), nullable=True),
        sa.Column('source_ref', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), nullable=False),
        sa.Column('rule_version', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=False, nullable=False)
    )

    op.create_table(
        'supplement_lifestyle_map',
        sa.Column('map_id', sa.String(50), primary_key=True),
        sa.Column('supplement_id', sa.String(50), sa.ForeignKey('supplements.supplement_id'), nullable=False),
        sa.Column('sleep_code', sa.String(50), sa.ForeignKey('sleep_categories.sleep_code'), nullable=False),
        sa.Column('match_type', sa.String(50), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False),
        sa.Column('source_id', sa.String(50), sa.ForeignKey('sources.source_id'), nullable=True),
        sa.Column('source_ref', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), nullable=False),
        sa.Column('rule_version', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=False, nullable=False)
    )

    op.create_table(
        'supplement_diet_compat',
        sa.Column('supplement_id', sa.String(50), sa.ForeignKey('supplements.supplement_id'), primary_key=True),
        sa.Column('diet_code', sa.String(50), sa.ForeignKey('diets.diet_code'), primary_key=True),
        sa.Column('compat_status', sa.String(50), nullable=False),
        sa.Column('source_id', sa.String(50), sa.ForeignKey('sources.source_id'), nullable=True),
        sa.Column('source_ref', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), nullable=False),
        sa.Column('last_reviewed_at', sa.String(50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True)
    )

    op.create_table(
        'supplement_allergen',
        sa.Column('supplement_id', sa.String(50), sa.ForeignKey('supplements.supplement_id'), primary_key=True),
        sa.Column('allergen_code', sa.String(50), sa.ForeignKey('allergens.allergen_code'), primary_key=True),
        sa.Column('relation', sa.String(100), nullable=True),
        sa.Column('source_id', sa.String(50), sa.ForeignKey('sources.source_id'), nullable=True),
        sa.Column('source_ref', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=False, nullable=False),
        sa.Column('notes', sa.Text(), nullable=True)
    )

    op.create_table(
        'safety_rules',
        sa.Column('rule_id', sa.String(50), primary_key=True),
        sa.Column('supplement_id', sa.String(50), sa.ForeignKey('supplements.supplement_id'), nullable=True),
        sa.Column('rule_type', sa.String(50), nullable=False),
        sa.Column('condition_code', sa.String(100), nullable=False),
        sa.Column('triggering_attribute', sa.String(100), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('safety_message', sa.Text(), nullable=False),
        sa.Column('source_id', sa.String(50), sa.ForeignKey('sources.source_id'), nullable=True),
        sa.Column('source_ref', sa.Text(), nullable=True),
        sa.Column('verification_status', sa.String(50), nullable=False),
        sa.Column('rule_version', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=False, nullable=False)
    )

    op.create_table(
        'scoring_config',
        sa.Column('criterion_id', sa.String(50), primary_key=True),
        sa.Column('criterion_code', sa.String(50), unique=True, nullable=False),
        sa.Column('criterion_name', sa.String(100), nullable=True),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('minimum_value', sa.Float(), default=0.0, nullable=False),
        sa.Column('maximum_value', sa.Float(), default=1.0, nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('rule_version', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False)
    )

    op.create_table(
        'criterion_value_rules',
        sa.Column('rule_id', sa.String(50), primary_key=True),
        sa.Column('criterion_code', sa.String(50), sa.ForeignKey('scoring_config.criterion_code'), nullable=False),
        sa.Column('condition', sa.Text(), nullable=True),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('rule_version', sa.String(50), nullable=True)
    )

    op.create_table(
        'system_config',
        sa.Column('config_key', sa.String(100), primary_key=True),
        sa.Column('config_value', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('rule_version', sa.String(50), nullable=True)
    )

    op.create_table(
        'explanation_templates',
        sa.Column('template_id', sa.String(50), primary_key=True),
        sa.Column('criterion_code', sa.String(50), nullable=False),
        sa.Column('match_value', sa.String(50), nullable=True),
        sa.Column('template_text', sa.Text(), nullable=False),
        sa.Column('required_attribute', sa.Text(), nullable=True),
        sa.Column('rule_version', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False)
    )


def downgrade():
    tables = [
        'explanation_templates', 'system_config', 'criterion_value_rules', 'scoring_config',
        'safety_rules', 'supplement_allergen', 'supplement_diet_compat', 'supplement_lifestyle_map',
        'supplement_activity_map', 'supplement_goal_map', 'supplements', 'sleep_categories',
        'activity_levels', 'medication_classes', 'conditions', 'allergens', 'diets', 'goals',
        'sources', 'recommendation_results'
    ]
    for t in tables:
        op.drop_table(t)

