"""add content to posts table

Revision ID: b860bc9bafe4
Revises: 9e166260eeca
Create Date: 2025-07-01 16:24:03.446938

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b860bc9bafe4"
down_revision: Union[str, Sequence[str], None] = "9e166260eeca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
