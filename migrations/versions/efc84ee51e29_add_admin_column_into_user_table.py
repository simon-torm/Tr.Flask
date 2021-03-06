"""Add admin column into User table

Revision ID: efc84ee51e29
Revises: 1c52fe962c8a
Create Date: 2021-08-26 22:31:58.742145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efc84ee51e29'
down_revision = '1c52fe962c8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'admin')
    # ### end Alembic commands ###
