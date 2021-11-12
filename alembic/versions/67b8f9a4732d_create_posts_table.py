"""create_posts_table

Revision ID: 67b8f9a4732d
Revises: c7b55c6dc497
Create Date: 2021-11-12 00:23:04.668501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67b8f9a4732d'
down_revision = 'c7b55c6dc497'
branch_labels = None
depends_on = None

table_name = 'posts'
table_name_users = 'posts'

def upgrade():
    op.create_table(table_name, 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(f'{table_name}_{table_name_users}_fk', source_table=table_name, referent_table=table_name_users, local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_table(table_name)
    pass