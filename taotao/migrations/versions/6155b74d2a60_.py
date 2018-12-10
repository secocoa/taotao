"""empty message

Revision ID: 6155b74d2a60
Revises: 
Create Date: 2018-12-08 20:25:27.082084

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6155b74d2a60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comment_ibfk_1', 'comment', type_='foreignkey')
    op.drop_column('comment', 'co_strategy')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('co_strategy', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('comment_ibfk_1', 'comment', 'strategy', ['co_strategy'], ['s_id'])
    # ### end Alembic commands ###