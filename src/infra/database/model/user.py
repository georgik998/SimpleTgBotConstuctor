from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.model import BaseDb

if TYPE_CHECKING:
    from src.infra.database.model import BotDb


class UserDb(BaseDb):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)

    bots: Mapped[list["BotDb"]] = relationship(
        'BotDb',
        back_populates='owner',
        cascade='all, delete-orphan'
    )
