from typing import List

from pylemmy import Lemmy
from sqlalchemy import insert, delete, select
from sqlalchemy.orm import Session

from command import GroupLemmyCommand, LemmyCommand
from models import KeywordList, Keyword


class KeywordCommand(GroupLemmyCommand):

    def __init__(self):
        self.commands = [KeywordListCommand(), KeywordWordCommand()]

    def key(self) -> str:
        return "keyword"


class KeywordListCommand(GroupLemmyCommand):

    def __init__(self):
        self.commands = [CreateKeywordListCommand(), DeleteKeywordListCommand(), ListKeywordListCommand()]

    def key(self) -> str:
        return "list"


class CreateKeywordListCommand(LemmyCommand):

    def key(self) -> str:
        return "create"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) != 1:
            return f"too few arguments, expected 1, got {len(args)}"

        session.execute(
            insert(KeywordList),
            [
                {'name': args[0]}
            ]
        )

        return f"created keyword list {args[0]}"


class DeleteKeywordListCommand(LemmyCommand):

    def key(self) -> str:
        return "delete"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) != 1:
            return f"too few arguments, expected 1, got {len(args)}"

        session.execute(
            delete(KeywordList)
            .where(KeywordList.name == args[0]),
        )

        return f"deleted keyword list {args[0]}"


class ListKeywordListCommand(LemmyCommand):

    def key(self) -> str:
        return "list"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        result = session.execute(
            select(KeywordList)
        )

        contents = ", ".join([f"\"{x.name}\"" for x in result.scalars()])
        return f"[{contents}]"


class KeywordWordCommand(GroupLemmyCommand):
    def __init__(self):
        self.commands = [CreateKeywordWordCommand(), DeleteKeywordWordCommand(), ListKeywordWordCommand()]

    def key(self) -> str:
        return "word"


class CreateKeywordWordCommand(LemmyCommand):

    def key(self) -> str:
        return "create"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) != 2:
            return f"too few arguments, expected 2, got {len(args)}"

        list_name = args[0]
        word = args[1]

        kl = session.execute(
            select(KeywordList)
            .where(KeywordList.name == list_name)
        ).fetchone()

        if kl is None:
            return f"no keyword list named \"{list_name}\" found"

        session.execute(
            insert(Keyword),
            [
                {'word': word, 'parent_id': kl.KeywordList.id}
            ]
        )

        return f"registered keyword \"{word}\" in list {list_name}"


class DeleteKeywordWordCommand(LemmyCommand):

    def key(self) -> str:
        return "delete"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) != 2:
            return f"too few arguments, expected 2, got {len(args)}"

        list_name = args[0]
        word = args[1]

        kl = session.execute(
            select(KeywordList)
            .where(KeywordList.name == list_name)
        ).fetchone()

        if kl is None:
            return f"no keyword list named \"{list_name}\" found"

        session.execute(
            delete(Keyword)
            .where(Keyword.parent_id == kl.KeywordList.id)
            .where(Keyword.word == word)
        )

        return f"unregistered keyword \"{word}\" in list {list_name}"


class ListKeywordWordCommand(LemmyCommand):
    def key(self) -> str:
        return "list"

    def execute(self, lemmy: Lemmy, session: Session, args: List[str]) -> str:
        if len(args) != 1:
            return f"too few arguments, expected 1, got {len(args)}"

        list_name = args[0]
        kl = session.execute(
            select(KeywordList)
            .where(KeywordList.name == list_name)
        ).fetchone()

        if kl is None:
            return f"no keyword list named \"{list_name}\" found"

        result = session.execute(
            select(Keyword)
            .where(Keyword.parent_id == kl.KeywordList.id)
        )
        contents = ", ".join([f"\"{x.word}\"" for x in result.scalars()])
        return f"[{contents}]"
