"""empty message

Revision ID: 07bcb5aec612
Revises: 2643d0f24285
Create Date: 2021-06-01 00:54:21.057214

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '07bcb5aec612'
down_revision = '2643d0f24285'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_stamp', sa.String(length=25), nullable=True))
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', mysql.VARCHAR(length=30), nullable=True))
        batch_op.drop_column('time_stamp')

    # ### end Alembic commands ###
