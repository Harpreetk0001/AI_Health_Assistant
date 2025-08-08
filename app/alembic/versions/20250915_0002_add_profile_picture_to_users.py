"""Add profile_picture to users table

Revision ID: 20250915_0002
Revises: 20250806_0001
Create Date: 2025-09-15 09:00:00
"""
from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision = '20250915_0002'
down_revision = '20250806_0001'
branch_labels = None
depends_on = None
def upgrade():
    # Adding a new column for profile picture URL or file path
    op.add_column(
        'users',
        sa.Column('profile_picture', sa.String(length=255), nullable=True)
    )
def downgrade():
    op.drop_column('users', 'profile_picture')
