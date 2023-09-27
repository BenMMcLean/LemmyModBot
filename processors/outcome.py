from typing import Dict, List

from processors import LemmyHandle, ContentResult


class Outcome:

    def execute(self, handle: LemmyHandle, extras: Dict[str, str]) -> ContentResult:
        return ContentResult.nothing()


class ListOutcome(Outcome):
    outcomes: List[Outcome]

    def __init__(self, outcomes: List[Outcome]):
        self.outcomes = outcomes

    def execute(self, handle: LemmyHandle, extras: Dict[str, str]) -> ContentResult:
        extras = {}
        flags = []
        for outcome in self.outcomes:
            result = outcome.execute(handle, extras)
            extras = {**extras, **result.extras}
            flags += result.flags
        return ContentResult(flags, extras)


class CommentOutcome(Outcome):
    message: str

    def __init__(self, message: str):
        self.message = message

    def execute(self, handle: LemmyHandle, extras: Dict[str, str]) -> ContentResult:
        handle.post_comment(self.message)
        return ContentResult.nothing()


class MessageOutcome(Outcome):
    message: str

    def __init__(self, message: str):
        self.message = message

    def execute(self, handle: LemmyHandle, extras: Dict[str, str]) -> ContentResult:
        handle.send_message_to_author(self.message)
        return ContentResult.nothing()


class RemoveOutcome(Outcome):

    def execute(self, handle: LemmyHandle, extras: Dict[str, str]) -> ContentResult:
        handle.remove_thing(extras['reason'] if 'reason' in extras else None)
        return ContentResult.nothing()


class PhashCommentOutcome(Outcome):

    def execute(self, handle: LemmyHandle, extras: Dict[str, str]) -> ContentResult:
        if 'phash' not in extras:
            return ContentResult.nothing()
        posts = handle.database.get_post_links_by_phash(extras['phash'])
        other_posts = ', '.join([f"[link]({post})" for post in posts])
        handle.post_comment(
            f"This post appears to be a duplicate of the following post{'' if len(posts) == 1 else 's'}: {other_posts}. "
            f"This could be a false positive (beep boop I am a robot).")
        return ContentResult.nothing()


class ToxicityFlagOutcome(Outcome):

    def execute(self, handle: LemmyHandle, extras: Dict[str, str]) -> ContentResult:
        pass
    