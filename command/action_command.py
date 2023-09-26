from typing import List

from pylemmy import Lemmy
from sqlalchemy import insert, delete, select
from sqlalchemy.orm import Session

from command import GroupLemmyCommand, LemmyCommand
from models import Action, ActionType


class ActionCommand(GroupLemmyCommand):

    def __init__(self):
        self.commands = [CreateActionCommand(), DeleteActionCommand(), ListActionCommand()]

    def key(self) -> str:
        return "action"


class CreateActionCommand(GroupLemmyCommand):

    def key(self) -> str:
        return "create"

    def __init__(self):
        self.commands = [
            CreateDeleteActionCommand(),
            CreateCommentActionCommand(),
            CreateReportActionCommand()
        ]


class CreateDeleteActionCommand(LemmyCommand):

    def key(self) -> str:
        return "delete"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) < 1:
            return f"too few arguments, expected 1, got {len(args)}"
        session.execute(
            insert(Action),
            [
                {'name': args[0], 'type': ActionType.DELETE}
            ],
        )
        return f"delete action {args[0]} created"


class CreateReportActionCommand(LemmyCommand):

    def key(self) -> str:
        return "report"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) < 1:
            return f"too few arguments, expected 1, got {len(args)}"
        session.execute(
            insert(Action),
            [
                {'name': args[0], 'type': ActionType.REPORT}
            ],
        )
        return f"report action {args[0]} created"


class CreateCommentActionCommand(LemmyCommand):

    def key(self) -> str:
        return "comment"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) != 2:
            return f"too few arguments, expected 2, got {len(args)}"
        session.execute(
            insert(Action),
            [
                {'name': args[0], 'type': ActionType.COMMENT, 'content': args[1]}
            ],
        )
        return f"comment action {args[0]} created"


class DeleteActionCommand(GroupLemmyCommand):
    def __init__(self):
        self.commands = [DeleteDeleteActionCommand(), DeleteReportActionCommand(), DeleteCommentActionCommand()]

    def key(self) -> str:
        return "delete"


class DeleteDeleteActionCommand(LemmyCommand):

    def key(self) -> str:
        return "delete"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) < 1:
            return f"too few arguments, expected 1, got {len(args)}"
        session.execute(
            delete(Action)
            .where(Action.name == args[0])
            .where(Action.type == ActionType.DELETE),
        )
        return f"delete action {args[0]} deleted"


class DeleteReportActionCommand(LemmyCommand):

    def key(self) -> str:
        return "report"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) < 1:
            return f"too few arguments, expected 1, got {len(args)}"
        session.execute(
            delete(Action)
            .where(Action.name == args[0])
            .where(Action.type == ActionType.REPORT),
        )
        return f"report action {args[0]} deleted"


class DeleteCommentActionCommand(LemmyCommand):

    def key(self) -> str:
        return "comment"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) != 1:
            return f"too few arguments, expected 1, got {len(args)}"
        session.execute(
            delete(Action)
            .where(Action.name == args[0])
            .where(Action.type == ActionType.COMMENT),
        )
        return f"comment action {args[0]} deleted"


class ListActionCommand(LemmyCommand):

    def key(self):
        return "list"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        result = session.execute(
            select(Action)
        )

        return "\n".join([f"Name: {x.name}, Type: {x.type}" for x in result.scalars()])
