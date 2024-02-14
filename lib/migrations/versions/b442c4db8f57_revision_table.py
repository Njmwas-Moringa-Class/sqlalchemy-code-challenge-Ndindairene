"""revision table

Revision ID: b442c4db8f57
Revises: 2723e7bbcf91
Create Date: 2024-02-14 12:15:15.086937

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer,ForeignKey,String


# revision identifiers, used by Alembic.
revision = 'b442c4db8f57'
down_revision = '2723e7bbcf91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('reviews',
        Column('id', Integer, primary_key=True),
        Column('comment', String),
        Column('star rating', Integer)
    )
    

def downgrade() -> None:
    pass
