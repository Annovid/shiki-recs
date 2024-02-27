import logging
from typing import Any, Optional
from requests.exceptions import HTTPError

import shikimori_api

from db.models import UserRate, Title, User
from utils.parser import ShikimoriParser


class ShikimoriClient:
    session: shikimori_api.Shikimori = shikimori_api.Shikimori()
    api: shikimori_api = session.get_api()

    @classmethod
    def get_user_rates(cls, user_id: int) -> list[UserRate]:
        user_rates: list[dict[str, Any]] = cls.api.user_rates.GET(
            user_id=user_id, target_type="Anime"
        )
        return ShikimoriParser.parse_user_rates(user_rates)

    @classmethod
    def get_title_info(cls, title_id: int) -> Optional[Title]:
        title_op: list[dict[str, Any]] = cls.api.animes.GET(ids=title_id)
        if not title_op:
            return
        title: dict[str, Any] = title_op[0]
        return ShikimoriParser.get_title(title)

    @classmethod
    def get_users(cls, page: int, limit: int) -> list[User]:
        # TODO: check all possibilities
        users: list[dict[str, Any]] = cls.api.users.GET(page=page, limit=limit)
        return [ShikimoriParser.parse_user(user) for user in users]

    @classmethod
    def get_user_id(cls, user_name: str) -> Optional[int]:
        users: list[dict[str, Any]] = cls.api.users.GET(search=user_name)
        users_exact: list[dict[str, Any]] = [
            user
            for user in users
            if user["nickname"].lower() == user_name.lower()
        ]
        return users_exact[0]["id"] if users_exact else None

    @classmethod
    def get_username_by_id(cls, user_id: int) -> Optional[str]:
        try:
            response: dict[str, Any] = cls.api.users(user_id).GET()
            return response["nickname"]
        except HTTPError:
            return None

    @classmethod
    def get_max_user_id(cls) -> int:
        min_users_cnt = 1_450_000
        max_users_cnt = 2_000_000

        l, r = min_users_cnt, max_users_cnt
        while r - l > 1:
            mid = (r + l) // 2
            username = cls.get_username_by_id(mid)
            if username:
                l = mid
            else:
                r = mid
        logging.debug(f"Max user id: {l}")
        return l
