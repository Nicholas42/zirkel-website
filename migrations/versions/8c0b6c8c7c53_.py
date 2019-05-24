"""empty message

Revision ID: 8c0b6c8c7c53
Revises: ab3fa73c0df6
Create Date: 2019-05-23 16:23:26.514179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c0b6c8c7c53'
down_revision = 'ab3fa73c0df6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_table('modules_per_user',
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('modules_per_user')
    op.drop_table('module')
    # ### end Alembic commands ###