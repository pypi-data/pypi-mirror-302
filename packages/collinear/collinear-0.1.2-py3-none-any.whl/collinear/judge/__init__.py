from collinear.judge.collinear_guard import CollinearGuard
from collinear.judge.veritas import Veritas


class Judge:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self._veritas = None
        self._collinear_guard = None

    @property
    def veritas(self):
        """
        Lazy-load Veritas service when accessed for the first time.
        Cache the result for subsequent accesses.
        """
        if self._veritas is None:
            self._veritas = Veritas(self.access_token)
        return self._veritas

    @property
    def collinear_guard(self):
        """
        Lazy-load Collinear Guard service when accessed for the first time.
        Cache the result for subsequent accesses.
        """
        if self._collinear_guard is None:
            self._collinear_guard = CollinearGuard(self.access_token)
        return self._collinear_guard
