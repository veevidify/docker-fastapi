"""Add column last_name to User model and dbschema

Revision ID: 14ca970985f2
Revises: d4867f3a4c0a
Create Date: 2021-10-28 07:00:52.046398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14ca970985f2'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_name', sa.String(), nullable=True))
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'last_name')
    # ### end Alembic commands ###
