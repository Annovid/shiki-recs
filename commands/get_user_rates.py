import datetime
import logging
import random
import time

from sqlalchemy.exc import PendingRollbackError

from commands import Command
from db.engine import SessionFactory
from db.helpful_requests import DBUtilities
from db.models import User, UserRate
from utils.client import ShikimoriClient
from utils.settings import settings


class GetUserRatesCommand(Command):
    def __init__(self, users_count: int = 1):
        super().__init__()
        self.users_count = users_count

    def execute(self):
        max_user_id = (
            ShikimoriClient.get_max_user_id()
            if settings.SCORE_EXACT_USER_CNT
            else settings.DEFAULT_USERS_CNT
        )
        # TODO: найти способ находить пользователей с большим количеством
        #  тайтлов
        user_ids: list[int] = [
            random.randint(1, max_user_id) for _ in range(self.users_count)
        ]
        local_user_ids: list[int] = DBUtilities.get_all_user_ids()
        logging.debug(f"Already processed {len(local_user_ids)} users")
        user_ids = sorted(list(set(user_ids) - set(local_user_ids)))
        logging.debug(f"user_ids: {user_ids}")
        # TODO: посмотреть, можно ли получать оценки для нескольких
        #  пользователей за один запрос
        for user_id in user_ids:
            user_rates: list[UserRate] = ShikimoriClient.get_user_rates(
                user_id
            )
            self.export_user_rates(user_id, user_rates)
            time.sleep(settings.SLEEP_TIME)

    @classmethod
    def export_user_rates(cls, user_id: int, user_rates: list[UserRate]):
        logging.debug(f"Found {len(user_rates)} rates for user {user_id}")
        user = User(
            id=user_id,
            is_processed=True,
            process_datetime=datetime.datetime.now(),
        )
        DBUtilities.add_entities([user] + user_rates)