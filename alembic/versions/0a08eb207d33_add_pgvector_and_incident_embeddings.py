"""add pgvector and incident embeddings

Revision ID: 0a08eb207d33
Revises: 49235e9ca726
Create Date: 2026-03-06 22:23:31.109611
"""
from typing import Sequence, Union


from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '0a08eb207d33'
down_revision: Union[str, None] = '49235e9ca726'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable the pgvector extension in PostgreSQL
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Add embedding column — 1536 dimensions matches OpenAI's text-embedding-3-small model
    op.add_column('safety_incidents', sa.Column('embedding', Vector(1536), nullable=True))
    

def downgrade() -> None:
    op.drop_column('safety_incidents', 'embedding')
    op.execute('DROP EXTENSION IF EXISTS vector')