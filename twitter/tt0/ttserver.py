import time

import zmq

from server import Repository, Tweet
from ttserverpubsub import ServerPubSub

REPO = Repository()


def signup(user):
    REPO.add_user(user)
    return f"Bem-vindo, {user}"


def tweet(user, text):
    return str(REPO.add_tweet(Tweet(user, text)).uuid)


def tweet(user, text):
    return str(REPO.add_tweet(Tweet(user, text)).msg)


def follow(user, other):
    REPO.add_follow(user, other)
    return f"{user} seguindo {other}"


def followers(username):
    return REPO.get_masters(username)


def read(user):
    return "\n".join(f"{t.user}: {t.msg}" for t in REPO.get_tweets_from(user))


COMMANDS = dict(
    signup=signup,
    tweet=tweet,
    follow=follow,
    read=read,
    followers=followers,
)


class Server:
    def __init__(self) -> None:
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5557")
        self.pubsub = ServerPubSub()

    def run(self):
        while True:
            #  Wait for next request from client
            message = self.socket.recv()
            print(f"SERVER: Received request: {message}")

            reply = "\n"

            try:
                # import ipdb

                # ipdb.set_trace()

                cmd, user, *arg = message.decode("utf-8").split(" ", maxsplit=2)
                command = COMMANDS[cmd]
                reply = command(user, *arg)

                if cmd == "tweet":
                    self.pubsub.send_tweet(user, reply)
                elif cmd == "followers":
                    if reply:
                        reply = ",".join(reply)
                    else:
                        reply = ""

            except Exception as e:
                reply = "ERRO: " + str(e)
            #  Do some 'work'
            time.sleep(0.01)

            #  Send reply back to client
            self.socket.send_string(reply)


if __name__ == "__main__":
    server = Server()
    server.run()
