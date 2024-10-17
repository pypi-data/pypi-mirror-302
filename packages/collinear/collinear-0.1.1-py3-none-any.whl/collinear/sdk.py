from typing import Literal, overload
from collinear.judge import Judge


class Collinear:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self._judge = None

    @property
    def judge(self):
        """
        Lazy-load Veritas service when accessed for the first time.
        Cache the result for subsequent accesses.
        """
        if self._judge is None:
            self._judge = Judge(self.access_token)
        return self._judge
