import pytest
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import factories


@dataclass
class Tweet:
    user: str
    msg: str
    uuid: UUID = field(
        default_factory=lambda: factories.uuid()
    )
    created_at: datetime = field(
        default_factory=lambda: factories.now()
    )
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

        self.users[user] = {MSGS: [], FOLLOWING: set()}

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
        if user not in self.users:
            raise ValueError("Sei quem é não.")

        return self.users[user][MSGS]

    def get_masters(self, user):
        return self.users[user][FOLLOWING]



def test_repository(mocker):
    repo = Repository()

    repo.add_user("hb")
    assert repo.users == {"hb": {MSGS: [], FOLLOWING: set()}}

    with pytest.raises(ValueError):
        repo.add_user("hb")

    _now = mocker.spy(factories, 'now')
    _uuid = mocker.spy(factories, 'uuid')

    t = repo.add_tweet(Tweet("hb", "a"))

    assert vars(t) == dict(
        user="hb",
        msg="a",
        created_at=_now.spy_return,
        uuid=_uuid.spy_return,
        likes=0
    )

    repo.add_user("helinho")
    repo.add_follow("hb", "helinho")
    assert "helinho" in repo.users["hb"][FOLLOWING]

    repo.add_tweet(Tweet("helinho", "b"))

    tts = repo.get_tweets_from("helinho")
    assert len(tts) == 1
    assert tts[0].msg == "b"


def test_get_tweet(mocker):
    _now = mocker.spy(factories, 'now')
    id = factories.uuid()

    t = get_tweet(id)

    assert vars(t) == dict(
        user="henriquebastos",
        msg="Olá, Mundo!",
        created_at=_now.spy_return,
        uuid=id,
        likes=0
    )


def test_post_tweet(mocker):
    _now = mocker.spy(factories, 'now')
    _uuid = mocker.spy(factories, 'uuid')

    t = post_tweet("henriquebastos", "Olá, Mundo!")

    assert vars(t) == dict(
        user="henriquebastos",
        msg="Olá, Mundo!",
        created_at=_now.spy_return,
        uuid=_uuid.spy_return,
        likes=0
    )


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
