from command import GroupLemmyCommand
from command.action_command import ActionCommand
from command.keyword_command import KeywordCommand


class RootCommand(GroupLemmyCommand):

    def __init__(self):
        self.commands = [ActionCommand(), KeywordCommand()]

    def key(self) -> str:
        return "root"
