"""empty message

Revision ID: f0f3ed815e42
Revises: d8c2c3a7c958
Create Date: 2021-06-11 10:14:50.950424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0f3ed815e42'
down_revision = 'd8c2c3a7c958'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('event_url', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('event_url')

    # ### end Alembic commands ###