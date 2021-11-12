"""create_users_table

Revision ID: c7b55c6dc497
Revises: 
Create Date: 2021-11-11 23:55:07.558121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7b55c6dc497'
down_revision = None
branch_labels = None
depends_on = None

table_name = "users"

def upgrade():
    op.create_table(table_name, 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table(table_name)
    pass
