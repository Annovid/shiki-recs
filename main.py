import logging

from commands.get_user_rates import GetUserRatesCommand
from utils.log import setup_logging
from utils.settings import settings


def main():
    GetUserRatesCommand(users_count=settings.USERS_COUNT).execute()


if __name__ == "__main__":
    setup_logging()

    logging.info("Script started")
    main()
    logging.info("Script finished")
