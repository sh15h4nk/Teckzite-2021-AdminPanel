"""empty message

Revision ID: d211b143f634
Revises: 6f6f6db68f1d
Create Date: 2021-06-04 09:00:08.219347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd211b143f634'
down_revision = '6f6f6db68f1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('current_id', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_team_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team_status', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_column('team_status')

    with op.batch_alter_table('current_id', schema=None) as batch_op:
        batch_op.drop_column('current_team_id')

    # ### end Alembic commands ###
