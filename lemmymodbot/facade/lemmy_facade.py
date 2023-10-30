import requests
from plemmy import LemmyHttp


class LemmyFacade:
    lemmy: LemmyHttp

    def __init__(self, lemmy: LemmyHttp):
        self.lemmy = lemmy

    def get_posts(self, name: str, page: int) -> requests.Response:
        return self.lemmy.get_posts(
            community_name=name,
            page=page
        )

    def get_comments(self, community: str, page: int) -> requests.Response:
        return self.lemmy.get_comments(
            community_name=community,
            page=page
        )
