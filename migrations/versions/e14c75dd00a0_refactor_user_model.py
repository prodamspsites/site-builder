"""Refactor User Model
This migration removes username and add more informations about confirmation.

Revision ID: e14c75dd00a0
Revises: 913e2a08a191
Create Date: 2016-09-23 13:54:08.700597

"""

# revision identifiers, used by Alembic.
revision = 'e14c75dd00a0'
down_revision = '913e2a08a191'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('temporary_token', sa.String(length=20), nullable=True))
    op.drop_constraint('user_username_key', 'user', type_='unique')
    op.drop_column('user', 'username')
    op.alter_column('user', 'password', existing_type=sa.VARCHAR(length=255), nullable=True)


def downgrade():
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.drop_column('user', 'temporary_token')
    op.drop_column('user', 'confirmed_at')
    op.drop_column('user', 'confirmed')
    op.alter_column('user', 'password', existing_type=sa.VARCHAR(length=255), nullable=False)