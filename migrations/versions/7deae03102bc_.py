"""empty message

Revision ID: 7deae03102bc
Revises: 7dba9165712c
Create Date: 2021-05-30 13:43:21.706323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7deae03102bc'
down_revision = '7dba9165712c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('CA', schema=None) as batch_op:
        batch_op.add_column(sa.Column('collegeId', sa.String(length=30), nullable=True))

    with op.batch_alter_table('current_id', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_ca_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('current_id', schema=None) as batch_op:
        batch_op.drop_column('current_ca_id')

    with op.batch_alter_table('CA', schema=None) as batch_op:
        batch_op.drop_column('collegeId')

    # ### end Alembic commands ###
