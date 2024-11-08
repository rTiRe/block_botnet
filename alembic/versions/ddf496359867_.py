"""empty message

Revision ID: ddf496359867
Revises: a55215e702eb
Create Date: 2024-11-05 21:45:22.658184

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ddf496359867'
down_revision: Union[str, None] = 'a55215e702eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('next_demolition', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'next_demolition')
    # ### end Alembic commands ###
