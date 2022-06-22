from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

import pytest

import factories


@dataclass(frozen=True)
class User:
    username: str


@dataclass
class Tweet:
    user: str
    msg: str
    uuid: UUID = field(default_factory=lambda: factories.uuid())
    created_at: datetime = field(default_factory=lambda: factories.now())
    likes: int = 0


MSGS = "msgs"
FOLLOWING = "following"


class Repository:
    def __init__(self):
        self.tweets = {}
        self.users = {}

    def add_user(self, user):
        if user in self.users:
            raise ValueError("Já tem, mané!")

        self.users[user] = {MSGS: list(), FOLLOWING: set()}

    def add_tweet(self, tweet):
        if tweet.user not in self.users:
            raise ValueError()

        self.users[tweet.user][MSGS].append(tweet)
        self.tweets[tweet.uuid] = tweet

        return tweet

    def add_follow(self, user, other):
        if user not in self.users:
            raise ValueError("Seguidor não existe.")

        if other not in self.users:
            raise ValueError("Master não existe.")

        self.users[user][FOLLOWING].add(other)

    def get_tweets_from(self, user):
        if not user in self.users:
            raise ValueError("Sei quem é não.")

        return self.users[user][MSGS]

    def get_masters(self, user):
        return self.users[user][FOLLOWING]


def post_tweet(user, msg):
    return Tweet(user, msg)


def get_tweet(uuid):
    return Tweet(user="henriquebastos", msg="Olá, Mundo!", uuid=uuid)


if __name__ == "__main__":
    import pytest

    pytest.main(["-s", __file__])
