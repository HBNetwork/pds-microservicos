import zmq
from ttclient import Client


def subscriber():
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://localhost:5554")

    while True:
        sub.setsockopt_string(zmq.SUBSCRIBE, "")
        msg = sub.recv_string()
        print(msg)


if __name__ == "__main__":
    import sys
    user = sys.argv[1]
    client = Client()
    client.signup(user)
    subscriber()
