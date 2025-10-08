# ONLY DEV SCRIPT !!!!
import asyncio

from src.infra.database.model import BaseDb
from src.infra.database import build_engine_and_session, postgres_settings

engine, async_session = build_engine_and_session(
    dsn=postgres_settings.POSTGRES_DSN,
    pool_size=1,
    max_overflow=1
)


async def main(base):
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)

        await conn.run_sync(base.metadata.create_all)


if __name__ == '__main__':
    input('THIS SCRIPT WILL RESET AND KILL DATABASE !!!\nYou sure ?')
    asyncio.run(main(BaseDb))

