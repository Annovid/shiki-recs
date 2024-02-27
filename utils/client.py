from typing import Any, Optional

import shikimori_api

from db.models import UserRate, Title, User
from utils.parser import ShikimoriParser


class ShikimoriClient:
    def __init__(self):
        self.session: shikimori_api.Shikimori = shikimori_api.Shikimori()
        self.api: shikimori_api = self.session.get_api()

    def get_user_rates(self, user_id: int) -> list[UserRate]:
        user_rates: list[dict[str, Any]] = self.api.user_rates.GET(
            user_id=user_id, target_type='Anime'
        )
        return ShikimoriParser.parse_user_rates(user_rates)

    def get_title_info(self, title_id: int) -> Optional[Title]:
        title_op: list[dict[str, Any]] = self.api.animes.GET(ids=title_id)
        if not title_op:
            return
        title: dict[str, Any] = title_op[0]
        return ShikimoriParser.get_title(title)

    def get_users(self, page: int, limit: int) -> list[User]:
        # TODO: check all possibilities
        users: list[dict[str, Any]] = self.api.users.GET(
            page=page, limit=limit
        )
        return [ShikimoriParser.parse_user(user) for user in users]

    def get_user_id(self, user_name: str) -> Optional[int]:
        users: list[dict[str, Any]] = self.api.users.GET(search=user_name)
        users_exact: list[dict[str, Any]] = [
            user for user in users
            if user['nickname'].lower() == user_name.lower()
        ]
        return users_exact[0]['id'] if users_exact else None


print(ShikimoriClient().get_user_id('Annovid'))
