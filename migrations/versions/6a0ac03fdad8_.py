"""empty message

Revision ID: 6a0ac03fdad8
Revises: 83ec7f6673d2
Create Date: 2019-05-30 00:52:45.533785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a0ac03fdad8'
down_revision = '83ec7f6673d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currently_working', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('currently_working')

    # ### end Alembic commands ###
