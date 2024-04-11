import datetime
from typing import Any

from db.models import UserRate, User, Title


class ShikimoriParser:
    @classmethod
    def get_title(cls, title: dict[str, Any]):
        return Title(
            id=title["id"],
            name=title["name"],
            timestamp=datetime.datetime.now(),
            name_rus=title["russian"],
            rate=title["score"],
            episodes=title["episodes"],
            kind=title["kind"],
            status=title["status"],
        )

    @classmethod
    def parse_user_rate(cls, user_rate: dict[str, Any]):
        return UserRate(
            user_id=user_rate["user_id"],
            title_id=user_rate["target_id"],
            rate=user_rate["score"],
        )

    @classmethod
    def parse_user_rates(cls, user_rates: list[dict[str, Any]]):
        return [cls.parse_user_rate(rate) for rate in user_rates]

    @classmethod
    def parse_user(cls, user: dict[str, Any]):
        return User(
            id=user["id"],
            name=user["nickname"],
            timestamp=datetime.datetime.now(),
        )
