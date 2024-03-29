"""empty message

Revision ID: ab3fa73c0df6
Revises: 70b07c49ebd9
Create Date: 2019-05-21 20:02:32.338182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab3fa73c0df6'
down_revision = '70b07c49ebd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('next_subject', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('next_subject')

    # ### end Alembic commands ###
