from enum import Enum
from typing import List


class ParseContext(Enum):
    NONE = 0
    STRING = 1


class CommandParser:
    out: List[str] = []
    current_token = ""
    context = ParseContext.NONE

    def parse(self, command: str) -> List[str]:
        for e in command:
            if e == "\"":
                if self.context == ParseContext.STRING:
                    self.context = ParseContext.NONE
                    self._push_token()
                    continue
                else:
                    self.context = ParseContext.STRING
                    self._push_token()
                    continue

            if e == " " and self.context != ParseContext.STRING:
                self._push_token()
                continue

            self.current_token += e

        self._push_token()
        print(self.out)
        return self.out

    def _push_token(self):
        if len(self.current_token) < 1:
            return
        self.out += [self.current_token]
        self.current_token = ""
