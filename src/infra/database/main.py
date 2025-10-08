from typing import Tuple

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession


def build_engine_and_session(
        dsn: str,
        pool_size: int,
        max_overflow: int,
        echo: bool = False,
) -> Tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        url=dsn,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    return engine, session_factory

