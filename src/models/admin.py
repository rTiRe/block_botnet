from sqlalchemy import Integer, UUID, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from src.models.meta import Base

class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
