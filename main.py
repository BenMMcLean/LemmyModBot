import os

from command import RootCommand
from command.action_command import ActionCommand
from command.command_parser import CommandParser
from database import session_scope
from lemmybot import LemmyBot


if __name__ == "__main__":
    with session_scope() as session:
        # print(RootCommand().execute(None, session, CommandParser().parse("keyword list create test")))
        print(RootCommand().execute(None, session, CommandParser().parse("keyword list delete test")))
    # bot = LemmyBot()
    # bot.run()
