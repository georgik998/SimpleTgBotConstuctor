from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer, Text, text, ForeignKey, Boolean, String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.model import BaseDb

if TYPE_CHECKING:
    from src.infra.database.model import UserDb


class BotDb(BaseDb):
    __tablename__ = 'bots'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    api_token: Mapped[str] = mapped_column(String(46), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)
    owner_tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('FALSE'))
    config_file_path: Mapped[str] = mapped_column(Text, nullable=False)

    owner: Mapped["UserDb"] = relationship(
        'UserDb',
        back_populates='bots'
    )
