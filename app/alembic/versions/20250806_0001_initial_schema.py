"""Initial schema

Revision ID: 20250806_0001
Revises: 
Create Date: 2025-08-06 10:00:00

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '20250806_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # USER table
    op.create_table(
        'users',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('elderly', 'caregiver', 'admin', name='userrole'), nullable=False),
        sa.Column('language_preference', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    # HEALTH VITAL table
    op.create_table(
        'health_vitals',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('blood_pressure', sa.String(length=20)),
        sa.Column('heart_rate', sa.Integer),
        sa.Column('hydration_level', sa.Float),
        sa.Column('sleep_hours', sa.Float),
        sa.Column('step_count', sa.Integer),
    )

    # FALL EVENT
    op.create_table(
        'fall_events',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('location', sa.String(length=255)),
        sa.Column('severity', sa.String(length=50)),
    )

    # EMERGENCY CONTACT
    op.create_table(
        'emergency_contacts',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('name', sa.String(length=100)),
        sa.Column('phone', sa.String(length=20)),
        sa.Column('relationship', sa.String(length=50)),
    )

    # MEDICATION
    op.create_table(
        'medications',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('medication_name', sa.String(length=100)),
        sa.Column('dosage', sa.String(length=50)),
        sa.Column('schedule', sa.String(length=100)),
    )

    # REMINDER LOG
    op.create_table(
        'reminder_logs',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('reminder_type', sa.String(length=50)),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20)),
    )

    # CONVERSATION LOG
    op.create_table(
        'conversation_logs',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('message', sa.Text),
        sa.Column('source', sa.String(length=50)),  # voice/text
    )

    # ACTIVITY LOG
    op.create_table(
        'activity_logs',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('activity', sa.String(length=100)),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )

    # DEVICE INTEGRATION
    op.create_table(
        'device_integrations',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('device_name', sa.String(length=100)),
        sa.Column('integration_status', sa.String(length=50)),
        sa.Column('last_synced', sa.DateTime()),
    )

    # SUGGESTION
    op.create_table(
        'suggestions',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('content', sa.Text),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )

    # MENTAL HEALTH LOG
    op.create_table(
        'mental_health_logs',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('mood', sa.String(length=50)),
        sa.Column('notes', sa.Text),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )

    # UI PREFERENCE
    op.create_table(
        'ui_preferences',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('theme', sa.String(length=20)),  # light/dark
        sa.Column('font_size', sa.String(length=10)),
        sa.Column('language', sa.String(length=10)),
    )


def downgrade():
    # Drop in reverse order to maintain FK integrity
    op.drop_table('ui_preferences')
    op.drop_table('mental_health_logs')
    op.drop_table('suggestions')
    op.drop_table('device_integrations')
    op.drop_table('activity_logs')
    op.drop_table('conversation_logs')
    op.drop_table('reminder_logs')
    op.drop_table('medications')
    op.drop_table('emergency_contacts')
    op.drop_table('fall_events')
    op.drop_table('health_vitals')
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS userrole')
