from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251022_0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True)
    )

    op.create_table(
        'vitals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('hydration', sa.Float),
        sa.Column('sleep', sa.Float),
        sa.Column('heartbeat', sa.Float),
        sa.Column('bp_systolic', sa.Float),
        sa.Column('bp_diastolic', sa.Float),
        sa.Column('steps', sa.Integer),
        sa.Column('timestamp', sa.DateTime)
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('tag', sa.String(length=100)),
        sa.Column('status', sa.String(length=50)),
        sa.Column('due_datetime', sa.DateTime)
    )

    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('relationship', sa.String(length=255)),
        sa.Column('phone', sa.String(length=100)),
        sa.Column('email', sa.String(length=255)),
        sa.Column('profile', sa.String(length=255)),
        sa.Column('favourite', sa.Boolean)
    )

    op.create_table(
        'ml_results',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('symptom_input', sa.Text),
        sa.Column('predicted_output', sa.Text),
        sa.Column('created_at', sa.DateTime)
    )

    op.create_table(
        'logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('action', sa.Text),
        sa.Column('timestamp', sa.DateTime)
    )

def downgrade():
    op.drop_table('logs')
    op.drop_table('ml_results')
    op.drop_table('contacts')
    op.drop_table('tasks')
    op.drop_table('vitals')
    op.drop_table('users')
