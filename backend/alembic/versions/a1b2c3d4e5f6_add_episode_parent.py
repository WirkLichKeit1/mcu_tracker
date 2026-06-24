"""add episode_number and parent_id to content

Revision ID: a1b2c3d4e5f6
Revises: 3bd20cd1250a
Create Date: 2026-06-24 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = "3bd20cd1250a"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        "content",
        sa.Column("episode_number", sa.Integer(), nullable=True),
    )
    op.add_column(
        "content",
        sa.Column("parent_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_content_parent_id",
        "content",
        "content",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )

def downgrade() -> None:
    op.drop_constraint("fk_content_parent_id", "content", type_="foreignkey")
    op.drop_column("content", "parent_id")
    op.drop_column("content", "episode_number")