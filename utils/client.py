from typing import Any, Optional

import shikimori_api

from utils.models import UserRate, User, Title
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

    def get_user_ids(self, page: int, limit: int) -> list[int]:
        # TODO: check all possibilities
        users: list[dict[str, Any]] = self.api.users.GET(
            page=page, limit=limit
        )
        return [user['id'] for user in users]


if __name__ == '__main__':
    client: ShikimoriClient = ShikimoriClient()
    # print(client.get_user_rates(123))
    print(client.get_user_ids(1, 100))
