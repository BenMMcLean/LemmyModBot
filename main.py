from lemmybot import LemmyBot
from processors import ToxicityProcessor, BlacklistProcessor, PhashProcessor, TitleConformityProcessor

if __name__ == "__main__":
    bot = LemmyBot([
        ToxicityProcessor(),
        BlacklistProcessor(["tranny", "trap", "fag", "faggot"]),
        PhashProcessor(),
        TitleConformityProcessor(
            ".* \\(.+\\)",
            "It appears your post does not contain an artist in the title. Please update your post accordingly."
        )
    ])
    bot.run()