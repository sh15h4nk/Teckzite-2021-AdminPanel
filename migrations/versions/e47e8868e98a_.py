"""empty message

Revision ID: e47e8868e98a
Revises: 9b8dd6616b46
Create Date: 2021-06-04 19:05:26.504351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e47e8868e98a'
down_revision = '9b8dd6616b46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eventId', sa.String(length=7), nullable=True))
        batch_op.add_column(sa.Column('event_title', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_column('event_title')
        batch_op.drop_column('eventId')

    # ### end Alembic commands ###
