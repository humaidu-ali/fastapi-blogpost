"""add last few columns to posts table

Revision ID: efaed15bc876
Revises: 13c4bf9e5ba3
Create Date: 2022-02-21 09:49:02.532785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efaed15bc876'
down_revision = '13c4bf9e5ba3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='True'),)
    
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
