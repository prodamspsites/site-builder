"""Initialize Database

Revision ID: c92fce5bcfa5
Revises: None
Create Date: 2016-10-04 16:49:45.924109

"""

# revision identifiers, used by Alembic.
revision = 'c92fce5bcfa5'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_role_created_at'), 'role', ['created_at'], unique=False)

    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('confirmed', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('confirmed_at', sa.DateTime(), nullable=True),
        sa.Column('current_login_at', sa.DateTime(), nullable=True),
        sa.Column('login_count', sa.Integer(), nullable=True),
        sa.Column('temporary_token', sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)

    op.create_table('invite',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('host_id', sa.Integer(), nullable=True),
        sa.Column('guest_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_sent_at', sa.DateTime(), nullable=True),
        sa.Column('expire_at', sa.DateTime(), nullable=True),
        sa.Column('viewed_at', sa.DateTime(), nullable=True),
        sa.Column('accepted_at', sa.DateTime(), nullable=True),
        sa.Column('current_status', sa.Enum('criado', 'aceito', 'inválido', 'visualizado', 'enviado', 'reenviado', name='current_status'), nullable=True),
        sa.Column('sent_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['guest_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['host_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invite_accepted_at'), 'invite', ['accepted_at'], unique=False)
    op.create_index(op.f('ix_invite_created_at'), 'invite', ['created_at'], unique=False)
    op.create_index(op.f('ix_invite_expire_at'), 'invite', ['expire_at'], unique=False)
    op.create_index(op.f('ix_invite_last_sent_at'), 'invite', ['last_sent_at'], unique=False)
    op.create_index(op.f('ix_invite_viewed_at'), 'invite', ['viewed_at'], unique=False)

    op.create_table('user_role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'role_id', name='un_user_role')
    )
    op.create_index(op.f('ix_user_role_created_at'), 'user_role', ['created_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_user_role_created_at'), table_name='user_role')
    op.drop_table('user_role')

    op.drop_index(op.f('ix_invite_viewed_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_last_sent_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_expire_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_created_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_accepted_at'), table_name='invite')
    op.drop_table('invite')

    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_table('user')

    op.drop_index(op.f('ix_role_created_at'), table_name='role')
    op.drop_table('role')
