"""Create invite model

Revision ID: 5105c23bd2ac
Revises: e14c75dd00a0
Create Date: 2016-09-23 16:29:44.187403

"""

# revision identifiers, used by Alembic.
revision = '5105c23bd2ac'
down_revision = 'e14c75dd00a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('invite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=True),
    sa.Column('guest_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_sent_at', sa.DateTime(), nullable=True),
    sa.Column('expire_at', sa.DateTime(), nullable=True),
    sa.Column('viewed_at', sa.DateTime(), nullable=True),
    sa.Column('accepted_at', sa.DateTime(), nullable=True),
    sa.Column('current_status', sa.String(length=20), nullable=True),
    sa.Column('sent_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['guest_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['host_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invite_accepted_at'), 'invite', ['accepted_at'], unique=False)
    op.create_index(op.f('ix_invite_created_at'), 'invite', ['created_at'], unique=False)
    op.create_index(op.f('ix_invite_viewed_at'), 'invite', ['viewed_at'], unique=False)
    op.create_index(op.f('ix_invite_expire_at'), 'invite', ['expire_at'], unique=False)
    op.create_index(op.f('ix_invite_last_sent_at'), 'invite', ['last_sent_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_invite_viewed_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_last_sent_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_expire_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_created_at'), table_name='invite')
    op.drop_index(op.f('ix_invite_accepted_at'), table_name='invite')
    op.drop_table('invite')
