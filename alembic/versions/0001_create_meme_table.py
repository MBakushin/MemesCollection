"""create meme table

Revision ID: 0001
Revises:
Create Date: 2023-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'memes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('image_url', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('memes')
