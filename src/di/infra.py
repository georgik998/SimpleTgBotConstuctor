from typing import AsyncIterator

from dishka import Provider, Scope, provide

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.deployment.service import IDeployService

from src.infra.database import build_engine_and_session
from src.infra.process_manager import ProcessDeployService


class DatabaseProvider(Provider):
    _active_sessions = set()

    def __init__(self, dsn: str, pool_size: int, max_overflow):
        super().__init__()
        self.engine, self.session_factory = build_engine_and_session(
            dsn=dsn,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    async def provide_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            yield session


class DeploymentServiceProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_deploy_service(self) -> IDeployService:
        return ProcessDeployService()
