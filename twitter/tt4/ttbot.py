import time
from queue import Queue
from threading import Thread

import zmq


class Bot:
    def __init__(self, cmd_queue):
        self.queue = cmd_queue
        self.user = None

        self.context = zmq.Context()

        self.req = self.context.socket(zmq.REQ)
        self.req.connect("tcp://localhost:5557")

        self.sub = self.context.socket(zmq.SUB)
        self.sub.connect("tcp://localhost:5554")

    def run_forever(self):
        assert self.user

        while True:
            if self.queue.empty():
                try:
                    msg = self.sub.recv_string(zmq.NOBLOCK)
                    print(msg)
                    print("> ", end="", flush=True)
                except zmq.Again:
                    pass
            else:
                message = self.queue.get()
                print(message)
                reply = self.send_command(message)

                if reply.startswith("following"):
                    self.subscribe(reply)
                self.queue.task_done()  # unblocks prompter

            time.sleep(0.1)

    def subscribe(self, reply):
        master = reply.split()[-1]
        self.sub.setsockopt_string(zmq.SUBSCRIBE, f"@{master}")

    def send_command(self, message):
        cmd, *arg = message.split(' ', maxsplit=1)
        command = ' '.join([cmd, self.user, *arg])
        self.req.send_string(command)
        reply = self.req.recv().decode()
        return reply

    def signup(self, username):
        self.user = username
        reply = self.send_command(f"signup")
        self.subscribe(username)
        return reply

    def read_tweets(self):
        while True:
            try:
                yield self.sub.recv_string(zmq.NOBLOCK)
            except zmq.Again:
                break


class Prompter(Thread):
    """Prompt user for command input.
    Runs in a separate thread so the main-thread does not block.
    """
    def __init__(self, cmd_queue):
        super().__init__()
        self.cmd_queue = cmd_queue

    def run(self):
        while True:
            cmd = input('> ')
            self.cmd_queue.put(cmd)
            self.cmd_queue.join()  # blocks until consumer calls task_done()


if __name__ == "__main__":
    import sys
    user = sys.argv[1]
    tts = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    wait = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    cmd_queue = Queue()

    client = Bot(cmd_queue=cmd_queue)

    client.signup(user)
    time.sleep(wait)
    for user in client.send_command("listusers").split("\n"):
        client.send_command(f"follow {user}")
        client.subscribe(user)

    for count in range(tts):
        for msg in client.read_tweets():
            pass #print(msg)
        client.send_command(f"tweet Msg {count}.")
