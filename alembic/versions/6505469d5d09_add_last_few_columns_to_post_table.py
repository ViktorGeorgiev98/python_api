"""add last few columns to post table

Revision ID: 6505469d5d09
Revises: 6ce969f178ee
Create Date: 2025-07-01 16:40:17.121510

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6505469d5d09"
down_revision: Union[str, Sequence[str], None] = "6ce969f178ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    # Note: The 'owner_id' column is not dropped here as it is not part
