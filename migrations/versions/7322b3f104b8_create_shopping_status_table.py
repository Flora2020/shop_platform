"""create_shopping_status_table

Revision ID: 7322b3f104b8
Revises: 2f3c38e267d0
Create Date: 2021-08-24 00:29:46.330567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7322b3f104b8'
down_revision = '2f3c38e267d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shopping_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=60), nullable=False),
    sa.Column('insert_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shopping_status')
    # ### end Alembic commands ###