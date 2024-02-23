from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=True)
    )

    op.create_table(
        'titles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=True),
        sa.Column('name_rus', sa.String(64), nullable=False),
        sa.Column('rate', sa.String(10), nullable=False),
        sa.Column('episodes', sa.Integer, nullable=True),
        sa.Column('kind', sa.String(20), nullable=False),
        sa.Column('status', sa.String(20), nullable=False)
    )

    op.create_table(
        'user_rates',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('title_id', sa.Integer, sa.ForeignKey('titles.id'), primary_key=True),
        sa.Column('rate', sa.Integer, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('user_rates')
    op.drop_table('titles')
    op.drop_table('users')
