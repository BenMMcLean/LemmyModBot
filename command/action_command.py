from typing import List

from pylemmy import Lemmy
from sqlalchemy.orm import Session

from command import GroupLemmyCommand, LemmyCommand


class ActionCommand(GroupLemmyCommand):

    def __init__(self):
        self.commands = [CreateActionCommand()]
        pass

    def key(self) -> str:
        return "action"


class CreateActionCommand(LemmyCommand):

    def key(self) -> str:
        return "create"


    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        pass
