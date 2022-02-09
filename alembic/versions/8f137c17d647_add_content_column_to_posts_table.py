"""add content column to posts table

Revision ID: 8f137c17d647
Revises: ba4627f5a59f
Create Date: 2022-02-21 09:23:12.358607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f137c17d647'
down_revision = 'ba4627f5a59f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False)) 
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
