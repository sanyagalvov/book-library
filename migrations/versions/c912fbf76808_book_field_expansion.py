"""book field expansion

Revision ID: c912fbf76808
Revises: e8eb403cad16
Create Date: 2020-05-01 21:09:28.595235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c912fbf76808'
down_revision = 'e8eb403cad16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('description', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'description')
    # ### end Alembic commands ###
