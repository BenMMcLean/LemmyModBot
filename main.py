import os

from command.action_command import ActionCommand
from command.command_parser import CommandParser
from database import session_scope
from lemmybot import LemmyBot


if __name__ == "__main__":
    with session_scope() as session:
        print(ActionCommand().execute(None, session, CommandParser().parse("list")))
    # bot = LemmyBot()
    # bot.run()
