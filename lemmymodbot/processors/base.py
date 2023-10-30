from typing import List, Any, Optional

from lemmymodbot import LemmyHandle


class ContentType:
    POST_TITLE = 0
    POST_BODY = 1
    POST_LINK = 2
    COMMENT = 3


class Content:
    community: str
    content: str
    actor_id: str
    type: ContentType

    def __init__(self, community: str, content: str, actor_id: str, type: ContentType):
        self.community = community
        self.content = content
        self.actor_id = actor_id
        self.type = type


class ContentResult:
    flags: List[str]
    extras: Optional[Any]

    def __init__(self, flags: List[str], extras: Optional[Any]):
        self.flags = flags
        self.extras = extras

    @staticmethod
    def nothing():
        return ContentResult([], None)


class Processor:

    def setup(self) -> None:
        pass

    def execute(self, content: Content, handle: LemmyHandle) -> ContentResult:
        return ContentResult.nothing()



