"""add census verification tokens table

Revision ID: 0019
Revises: 0018
Create Date: 2026-01-08

"""
from alembic import op
import sqlalchemy as sa

revision = '20260108_0019'
down_revision = '20260108_0018'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'census_verification_tokens',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('token', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('census_record_id', sa.Integer(), sa.ForeignKey('insurance_census_records.id', ondelete='CASCADE'), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id', ondelete='SET NULL'), nullable=True),
        sa.Column('is_used', sa.Boolean(), default=False, nullable=False),
        sa.Column('is_expired', sa.Boolean(), default=False, nullable=False),
        sa.Column('email_sent', sa.Boolean(), default=False, nullable=False),
        sa.Column('email_sent_at', sa.DateTime(), nullable=True),
        sa.Column('email_address', sa.String(255), nullable=True),
        sa.Column('verified', sa.Boolean(), default=False, nullable=False),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('updates_submitted', sa.Boolean(), default=False, nullable=False),
        sa.Column('reminder_count', sa.Integer(), default=0, nullable=False),
        sa.Column('last_reminder_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('created_by', sa.String(50), nullable=True),
    )
    
    # Create indexes for common queries
    op.create_index('ix_census_verification_census_record', 'census_verification_tokens', ['census_record_id'])
    op.create_index('ix_census_verification_employee', 'census_verification_tokens', ['employee_id'])
    op.create_index('ix_census_verification_verified', 'census_verification_tokens', ['verified'])


def downgrade() -> None:
    op.drop_index('ix_census_verification_verified')
    op.drop_index('ix_census_verification_employee')
    op.drop_index('ix_census_verification_census_record')
    op.drop_table('census_verification_tokens')
