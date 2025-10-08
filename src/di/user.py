from sqlalchemy.ext.asyncio import AsyncSession

from dishka import Provider, Scope, provide, FromDishka

from src.application.user.repository import IUseRepo
from src.infra.database.repository.user import SqlUserRepo
from src.application.user.interactor import (
    CreateUserInteractor
)


class UserRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_user_repo(self, session: FromDishka[AsyncSession]) -> IUseRepo:
        return SqlUserRepo(session)


class UserInteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_create_user_interactor(self, user_repo: FromDishka[IUseRepo]) -> CreateUserInteractor:
        return CreateUserInteractor(user_repo=user_repo)

