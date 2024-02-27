import sqlalchemy as sa
from sqlalchemy.exc import PendingRollbackError

from commands import Command
from db.engine import SessionFactory
from db.models import User, UserRate
from utils.client import ShikimoriClient


class GetUserRatesCommand(Command):
    def __init__(self, args: list[str]):
        super().__init__(args)

    def execute(self):
        with (SessionFactory() as session):
            user_ids: list[str] = session.query(User.id).filter(
                User.is_processed == False
            ).all()
            user_ids = user_ids[:5]
        for user_id in user_ids:
            # if
            user_rates = self.download_user_rates(user_id)
            with SessionFactory() as session:
                [session.add(user_rate) for user_rate in user_rates]
                try:
                    session.commit()
                except PendingRollbackError:
                    session.rollback()

    @staticmethod
    def download_user_rates(user_id: int) -> list[UserRate]:
        return ShikimoriClient().get_user_rates(user_id)
