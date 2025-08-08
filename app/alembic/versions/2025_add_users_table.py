"""create user table

Revision ID: 20250808_create_user_table
Revises:
Create Date: 2025-08-08 11:00:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid
# revision identifiers, used by Alembic
revision: str = "20250808_create_user_table"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
def downgrade() -> None:
    op.drop_table("user")
