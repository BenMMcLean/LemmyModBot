from io import BytesIO
from typing import Union

import imagehash
import requests
from PIL import Image
from pylemmy import Lemmy
from pylemmy.models.comment import Comment
from pylemmy.models.post import Post

from lemmymodbot import LemmyModHttp, config
from lemmymodbot.database import Database


class LemmyHandle:

    def __init__(self, lemmy: Lemmy, elem: Union[Post, Comment], database: Database):
        self.elem = elem
        self.lemmy = lemmy
        self.lemmy_http = LemmyModHttp(lemmy)
        self.database = database

    def send_message_to_author(self, content: str):
        if config.debug_mode:
            print(f"{content}")
            return
        actor_id = self.elem.post_view.post.creator_id if isinstance(self.elem, Post) else self.elem.comment_view
        self.lemmy_http.send_message(actor_id, f"{content}\n\nMod bot (with L plates)")

    def post_comment(self, content: str):
        if config.debug_mode:
            print(f"{content}")
            return
        self.elem.create_comment(f"{content}\n\nMod bot (with L plates)")

    def remove_thing(self, reason: str):
        if config.debug_mode:
            print(f"Remove {reason}")
            return
        if isinstance(self.elem, Post):
            self.lemmy_http.remove_post(self.elem.post_view.post.id, reason)
        elif isinstance(self.elem, Comment):
            self.lemmy_http.remove_comment(self.elem.comment_view.comment.id, reason)

    def fetch_image(self, url: str) -> (Image, str):
        img = Image.open(BytesIO(requests.get(url).content))
        return img, str(imagehash.phash(img))
