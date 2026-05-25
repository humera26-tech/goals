"""create timesheet table

Revision ID: create_timesheet_001
Revises: ccf2b8eaf755
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'create_timesheet_001'
down_revision: Union[str, Sequence[str], None] = 'ccf2b8eaf755'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create timesheet table."""
    op.create_table(
        'timesheets',
        sa.Column('timesheet_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('work_date', sa.DateTime(), nullable=False),
        sa.Column('hours_worked', sa.Float(), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='Pending'),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('timesheet_id')
    )
    op.create_index(op.f('ix_timesheets_timesheet_id'), 'timesheets', ['timesheet_id'], unique=False)


def downgrade() -> None:
    """Drop timesheet table."""
    op.drop_index(op.f('ix_timesheets_timesheet_id'), table_name='timesheets')
    op.drop_table('timesheets')
