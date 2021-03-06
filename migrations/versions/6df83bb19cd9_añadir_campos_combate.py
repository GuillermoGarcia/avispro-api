"""Añadir campos combate

Revision ID: 6df83bb19cd9
Revises: 41e7a9814ce5
Create Date: 2019-06-18 18:15:35.046130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6df83bb19cd9'
down_revision = '41e7a9814ce5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('combate', sa.Column('iniciativa', sa.Integer(), nullable=False))
    op.add_column('combate', sa.Column('orden', sa.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('combate', 'orden')
    op.drop_column('combate', 'iniciativa')
    # ### end Alembic commands ###
