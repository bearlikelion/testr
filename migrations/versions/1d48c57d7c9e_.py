"""empty message

Revision ID: 1d48c57d7c9e
Revises: f8e4f9dd2095
Create Date: 2020-10-28 19:30:00.051573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d48c57d7c9e'
down_revision = 'f8e4f9dd2095'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commserv',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('hostnamename', sa.String(length=120), nullable=True),
    sa.Column('servicepack', sa.String(length=120), nullable=True),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commserv')
    # ### end Alembic commands ###
