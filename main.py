import sys
from typing import Type

from commands import Command
from commands.get_user_rates import GetUserRatesCommand
from commands.get_users import GetUsersCommand

command_mapping: dict[str, Type[Command]] = {
    'get_users': GetUsersCommand,
    'get_user_rates': GetUserRatesCommand,
}


def main():
    if len(sys.argv) < 2:
        print("Use: `python main.py <command>`")
        sys.exit(1)

    command_name: str = sys.argv[1]
    args: list[str] = sys.argv[2:]
    command_cls: Type[Command] = command_mapping[command_name]
    command: Command = command_cls(args)
    command.execute()


if __name__ == '__main__':
    main()
