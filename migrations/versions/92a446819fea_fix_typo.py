"""fix typo

Revision ID: 92a446819fea
Revises: 7b4c0a26c8d1
Create Date: 2021-09-25 09:47:30.084031

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '92a446819fea'
down_revision = '7b4c0a26c8d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('order_ibfk_4', 'order', type_='foreignkey')
    op.drop_column('order', 'shopping_status_id')
    op.create_table('shipping_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=60), nullable=False),
    sa.Column('insert_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status')
    )
    op.add_column('order', sa.Column('shipping_status_id', sa.Integer(), nullable=True))
    op.create_foreign_key('order_ibfk_4', 'order', 'shipping_status', ['shipping_status_id'], ['id'])
    op.drop_table('shopping_status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('order_ibfk_4', 'order', type_='foreignkey')
    op.drop_column('order', 'shipping_status_id')
    op.create_table('shopping_status',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status', mysql.VARCHAR(length=60), nullable=False),
    sa.Column('insert_time', mysql.DATETIME(), nullable=False),
    sa.Column('update_time', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.add_column('order', sa.Column('shopping_status_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('order_ibfk_4', 'order', 'shopping_status', ['shopping_status_id'], ['id'])
    op.drop_table('shipping_status')
    # ### end Alembic commands ###