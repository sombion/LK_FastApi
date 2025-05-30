"""Edit Users

Revision ID: 061ea508d199
Revises: ce1a1f2382bf
Create Date: 2025-04-09 08:45:47.972845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '061ea508d199'
down_revision: Union[str, None] = 'ce1a1f2382bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('count_login', sa.Integer(), nullable=False, server_default="0"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'count_login')
    # ### end Alembic commands ###
