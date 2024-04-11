from commands import Command
from db.engine import SessionFactory
from db.models import User
from utils.client import ShikimoriClient


class GetUsersCommand(Command):
    def __init__(self, args: list[str]):
        super().__init__()
        self.users_count: int = int(args[0])

    def execute(self):
        users: list[User] = self.download_users(self.users_count)
        self.extract_users(users)

    @staticmethod
    def download_users(users_count) -> list[User]:
        return ShikimoriClient.get_users(page=2, limit=users_count)

    @staticmethod
    def extract_users(users: list[User]) -> None:
        with SessionFactory() as session:
            for user in users:
                session.add(user)
