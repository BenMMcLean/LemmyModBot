from typing import List
from pylemmy import Lemmy
from sqlalchemy.orm import Session


class LemmyCommand:

    def key(self) -> str:
        pass

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        pass


class GroupLemmyCommand(LemmyCommand):
    commands: List[LemmyCommand] = []
    documentation = ""

    def key(self) -> str:
        pass

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) < 1:
            return self.documentation

        for command in self.commands:
            if args[0] == command.key():
                return command.execute(lemmy, session, args[1:])

        return f"\"{args[0]}\" is not a recognised command for {self.key()}"
