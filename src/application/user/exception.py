class UserAlreadyExistException(Exception):
    def __init__(
            self,
            tg_id: int
    ):
        super().__init__(f'User with tg_id={tg_id} already exist')
