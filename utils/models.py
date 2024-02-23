from datetime import datetime
from typing import NamedTuple, Optional


class User(NamedTuple):
    id: int
    name: str
    timestamp: datetime


class Title(NamedTuple):
    id: int
    name: str
    timestamp: datetime
    name_rus: str
    rate: str
    # series_duration: int  # minutes
    episodes: Optional[int]
    kind: str
    status: str


class UserRate(NamedTuple):
    user_id: int
    title_id: int
    rate: int
