"""empty message

Revision ID: 27c69e983bb3
Revises: 
Create Date: 2021-02-17 21:50:03.882665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27c69e983bb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('branch', sa.String(length=5), nullable=False, server_default="def"))
        batch_op.alter_column('branch', server_default=None)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('branch')

    # ### end Alembic commands ###
