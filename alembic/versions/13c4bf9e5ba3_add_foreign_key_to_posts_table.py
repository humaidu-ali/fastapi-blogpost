"""add foreign-key to posts table

Revision ID: 13c4bf9e5ba3
Revises: acfc3a5ff9ae
Create Date: 2022-02-21 09:42:50.349723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13c4bf9e5ba3'
down_revision = 'acfc3a5ff9ae'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('postd', 'owner_id')
    pass
