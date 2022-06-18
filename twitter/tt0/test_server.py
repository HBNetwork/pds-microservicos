import pytest


from .server import (
    FOLLOWING,
    MSGS,
    Repository,
    Tweet,
    get_tweet,
    post_tweet,
)

from . import factories


def test_repository(mocker):
    repo = Repository()

    repo.add_user("hb")
    assert repo.users == {"hb": {MSGS: [], FOLLOWING: set()}}

    with pytest.raises(ValueError):
        repo.add_user("hb")

    _now = mocker.spy(factories, "now")
    _uuid = mocker.spy(factories, "uuid")

    t = repo.add_tweet(Tweet("hb", "a"))

    assert vars(t) == dict(
        user="hb", msg="a", created_at=_now.spy_return, uuid=_uuid.spy_return, likes=0
    )

    repo.add_user("helinho")
    repo.add_follow("hb", "helinho")
    assert "helinho" in repo.users["hb"][FOLLOWING]

    repo.add_tweet(Tweet("helinho", "b"))

    tts = repo.get_tweets_from("helinho")
    assert len(tts) == 1
    assert tts[0].msg == "b"


def test_get_tweet(mocker):
    _now = mocker.spy(factories, "now")
    id = factories.uuid()

    t = get_tweet(id)

    assert vars(t) == dict(
        user="henriquebastos",
        msg="Olá, Mundo!",
        created_at=_now.spy_return,
        uuid=id,
        likes=0,
    )


def test_post_tweet(mocker):
    _now = mocker.spy(factories, "now")
    _uuid = mocker.spy(factories, "uuid")

    t = post_tweet("henriquebastos", "Olá, Mundo!")

    assert vars(t) == dict(
        user="henriquebastos",
        msg="Olá, Mundo!",
        created_at=_now.spy_return,
        uuid=_uuid.spy_return,
        likes=0,
    )
