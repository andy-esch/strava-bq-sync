from stravabqsync.domain import StravaTokenSet
from stravabqsync.ports.out.read import ReadStravaToken


class MockStravaTokenRepo(ReadStravaToken):
    def __init__(self, token: StravaTokenSet):
        self.token = token

    @property
    def refresh(self):
        return self.token
