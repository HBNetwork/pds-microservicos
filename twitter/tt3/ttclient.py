import time
from queue import Queue
from threading import Thread

import zmq


class Client:
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
                # while True:
                #     try:
                #         msg = self.sub.recv_string(zmq.NOBLOCK)
                #         print(msg)
                #     except zmq.Again:
                #         break
                try:
                    msg = self.sub.recv_string(zmq.NOBLOCK)
                    print(msg)
                    print("> ", end="", flush=True)
                except zmq.Again:
                    pass
            else:
                message = self.queue.get()
                print(message)
                cmd, *arg = message.split(' ', maxsplit=1)
                command = ' '.join([cmd, self.user, *arg])
                self.req.send_string(command)
                reply = self.req.recv().decode()

                if reply.startswith("following"):
                    master = reply.split()[-1]
                    self.sub.setsockopt_string(zmq.SUBSCRIBE, master)
                self.queue.task_done()  # unblocks prompter

            time.sleep(0.1)

    def signup(self, username):
        self.user = username
        self.req.send_string(f"signup {username}")
        reply = self.req.recv()
        self.sub.setsockopt_string(zmq.SUBSCRIBE, f"@{username}")
        return reply

    def followers(self, username):
        self.req.send_string(f"followers {username}")
        return self.req.recv()


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

    cmd_queue = Queue()

    client = Client(cmd_queue=cmd_queue)
    prompter = Prompter(cmd_queue=cmd_queue)
    prompter.daemon = True

    client.signup(user)
    prompter.start()
    client.run_forever()
