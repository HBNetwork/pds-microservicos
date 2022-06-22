import time
import zmq
from server import Repository, Tweet

REPO = Repository()


def signup(user):
    REPO.add_user(user)
    return f"Bem-vindo, {user}"


def tweet(user, text):
    return str(REPO.add_tweet(Tweet(user, text)).uuid)


def follow(user, other):
    REPO.add_follow(user, other)
    return f"{user} seguindo {other}"


def read(user):
    return '\n'.join(f"{t.user}: {t.msg}" for t in REPO.get_tweets_from(user))


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")


COMMANDS = dict(signup=signup, tweet=tweet, follow=follow, read=read)

while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")

    reply = "\n"

    try:
        print(message)
        cmd, user, *arg = message.decode("utf-8").split(" ", maxsplit=2)
        command = COMMANDS[cmd]
        reply = command(user, *arg)
        print(reply)
    except Exception as e:
        reply = "ERRO: " + str(e)
    #  Do some 'work'
    time.sleep(0.01)

    #  Send reply back to client
    socket.send_string(reply)
