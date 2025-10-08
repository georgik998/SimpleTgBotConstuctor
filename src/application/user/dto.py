from dataclasses import dataclass


@dataclass
class UserDto:
    tg_id: int


@dataclass
class CreateUserDto:
    tg_id: int
