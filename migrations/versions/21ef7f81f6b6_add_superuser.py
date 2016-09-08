"""Add superuser for User models

Revision ID: 21ef7f81f6b6
Revises: 913e2a08a191
Create Date: 2016-09-08 10:22:37.063333

"""

# revision identifiers, used by Alembic.
revision = '21ef7f81f6b6'
down_revision = '913e2a08a191'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('superuser', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('user', 'superuser')
