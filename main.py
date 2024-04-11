import logging

from commands.get_user_rates import GetUserRatesCommand
from utils.log import setup_logging


def main():
    GetUserRatesCommand(user_count=100).execute()


if __name__ == "__main__":
    setup_logging()

    logging.info("Script started")
    main()
    logging.info("Script finished")
