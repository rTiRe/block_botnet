import uuid

from sqlalchemy import UUID, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.models.meta import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    subscription: Mapped[int] = mapped_column(BigInteger, nullable=True, default=None)
    waiting_invoice: Mapped[int] = mapped_column(BigInteger, nullable=True, default=None)
