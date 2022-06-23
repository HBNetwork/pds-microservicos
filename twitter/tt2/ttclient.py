import time

import zmq


class Client:
    def __init__(self):
        self.user = None

        self.context = zmq.Context()

        self.req = self.context.socket(zmq.REQ)
        self.req.connect("tcp://localhost:5557")

        self.sub = self.context.socket(zmq.SUB)
        self.sub.connect("tcp://localhost:5554")

        self.input = self.context.socket(zmq.REP)
        self.input.bind("tcp://*:5550")

    def run_forever(self):
        assert self.user

        while True:
            while True:
                try:
                    entrada = self.input.recv(zmq.NOBLOCK)
                except zmq.Again:
                    break

                message = entrada.decode("utf-8")
                print(message)
                cmd, *arg = message.split(' ', maxsplit=1)
                command = ' '.join([cmd, self.user, *arg])
                self.req.send_string(command)
                reply = self.req.recv()
                print("SERVER RESPONSE: ", reply)
                break
            time.sleep(0.1)

    def signup(self, username):
        self.user = username
        self.req.send_string(f"signup {username}")
        return self.req.recv()

    def followers(self, username):
        self.req.send_string(f"followers {username}")
        return self.req.recv()


if __name__ == "__main__":
    import sys
    user = sys.argv[1]
    client = Client()
    client.signup(user)
    client.run_forever()
