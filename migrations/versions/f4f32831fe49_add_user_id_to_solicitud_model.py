"""Add user_id to Solicitud model

Revision ID: f4f32831fe49
Revises: e676f81c226b
Create Date: 2025-03-18 02:02:43.032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4f32831fe49'
down_revision = 'e676f81c226b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('solicitud', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_solicitud_user_id', 'user', ['user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('solicitud', schema=None) as batch_op:
        batch_op.drop_constraint('fk_solicitud_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')