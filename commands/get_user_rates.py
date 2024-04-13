import datetime
import logging
import random

import sqlalchemy as sa
from sqlalchemy.exc import PendingRollbackError

from commands import Command
from db.engine import SessionFactory
from db.models import User, UserRate
from utils.client import ShikimoriClient

DEFAULT_USERS_CNT = 1_450_000
SCORE_EXACT_USER_CNT: bool = False


class GetUserRatesCommand(Command):
    def __init__(self, user_count: int = 1):
        super().__init__()
        self.user_count = user_count

    def execute(self):
        max_user_id = (
            ShikimoriClient.get_max_user_id()
            if SCORE_EXACT_USER_CNT
            else DEFAULT_USERS_CNT
        )
        # TODO: найти способ находить пользователей с большим количеством
        #  тайтлов
        user_ids: list[int] = [
            random.randint(1, max_user_id) for _ in range(self.user_count)
        ]
        with SessionFactory() as session:
            processed_ids: list[int] = (
                session.query(User.id)
                .filter(User.is_processed == sa.false())
                .all()
            )
            logging.debug(f"Already processed {len(processed_ids)} users")
            user_ids = sorted(list(set(user_ids) - set(processed_ids)))
        logging.debug(f"user_ids: {user_ids}")
        # TODO: посмотреть, можно ли получать оценки для нескольких
        #  пользователей за один запрос
        for user_id in user_ids:
            # TODO: переписать через ThreadPool, обрабатывать исключения
            user_rates: list[UserRate] = ShikimoriClient.get_user_rates(
                user_id
            )
            self.export_user_rates(user_id, user_rates)

    @staticmethod
    def export_user_rates(user_id: int, user_rates: list[UserRate]):
        logging.debug(f"Found {len(user_rates)} rates for user {user_id}")
        with SessionFactory() as session:
            session.add(
                User(
                    id=user_id,
                    is_processed=True,
                    process_datetime=datetime.datetime.now(),
                )
            )
            for user_rate in user_rates:
                session.add(user_rate)
            try:
                session.commit()
            except PendingRollbackError:
                session.rollback()
