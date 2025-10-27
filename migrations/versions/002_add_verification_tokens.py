"""Add verification tokens table

Revision ID: 002
Revises: 001
Create Date: 2024-01-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Create verification_tokens table
    op.create_table(
        'verification_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=100), nullable=False),
        sa.Column('token_type', sa.String(length=20), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for better query performance
    op.create_index('ix_verification_tokens_token', 'verification_tokens', ['token'], unique=True)
    op.create_index('ix_verification_tokens_user_id', 'verification_tokens', ['user_id'])

def downgrade():
    # Drop indexes
    op.drop_index('ix_verification_tokens_user_id', table_name='verification_tokens')
    op.drop_index('ix_verification_tokens_token', table_name='verification_tokens')
    
    # Drop table
    op.drop_table('verification_tokens')
