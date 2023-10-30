from io import BytesIO
from typing import Union, List

import imagehash
import requests
from PIL import Image
from plemmy import LemmyHttp
from plemmy.objects import Post, Comment

from lemmymodbot import Config, LemmyModHttp, bot_identifier
from lemmymodbot.database import Database


class LemmyHandle:
    def __init__(self, lemmy: LemmyHttp, elem: Union[Post, Comment], database: Database, config: Config):
        self.elem = elem
        self.lemmy = lemmy
        self.lemmy_http = LemmyModHttp(lemmy)
        self.database = database
        self.config = config

    def send_message_to_author(self, content: str):
        if self.config.debug_mode:
            print(f"{content}")
            return

        actor_id = self.elem.creator_id
        self.lemmy.create_private_message(f"{content}\n\n{bot_identifier}", actor_id)

    def post_comment(self, content: str):
        if self.config.debug_mode:
            print(f"{content}")
            return
        self.lemmy.create_comment(
            f"{content}\n\n{bot_identifier}",
            self.elem.id if isinstance(self.elem, Post) else self.elem.post_id,
            parent_id=self.elem.id if isinstance(self.elem, Comment) else None
        )

    def remove_thing(self, reason: str):
        if self.config.debug_mode:
            print(f"Remove {reason}")
            return

        if isinstance(self.elem, Post):
            self.lemmy.remove_post(self.elem.id, True, reason)
        elif isinstance(self.elem, Comment):
            self.lemmy.remove_comment(self.elem.id, True, reason)

    def report_post(self, flags: List[str]):
        reason = f"{bot_identifier} : " + ", ".join(flags)
        if isinstance(self.elem, Post):
            self.lemmy.create_post_report(self.elem.id, reason)
        elif isinstance(self.elem, Comment):
            self.lemmy.create_comment_report(self.elem.id, reason)

    @staticmethod
    def fetch_image(url: str) -> (Image, str):
        img = Image.open(BytesIO(requests.get(url).content))
        return img, str(imagehash.phash(img))


class LemmyHandleFactory:
    _lemmy: LemmyHttp
    _config: Config
    _database: Database

    def __init__(self, config: Config, database: Database):
        self._config = config
        self._lemmy = LemmyHttp(config.instance)
        self._lemmy.login(config.username, config.password)
        self._database = database

    def create(self, elem: Union[Post, Comment]) -> LemmyHandle:
        return LemmyHandle(self._lemmy, elem, self._database, self._config)
