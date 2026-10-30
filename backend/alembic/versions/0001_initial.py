"""initial tables"""
import sqlalchemy as sa
from alembic import op
revision, down_revision = "0001", None
def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer, primary_key=True), sa.Column("email", sa.String, nullable=False, unique=True), sa.Column("pw", sa.String, nullable=False))
    op.create_table("user_profiles", sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True), sa.Column("data", sa.JSON, nullable=False), sa.Column("updated_at", sa.DateTime))
    op.create_table("recommendation_runs", sa.Column("id", sa.Integer, primary_key=True), sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime), sa.Column("status", sa.String), sa.Column("snapshot", sa.JSON), sa.Column("result", sa.JSON))
def downgrade():
    for t in ("recommendation_runs", "user_profiles", "users"): op.drop_table(t)
