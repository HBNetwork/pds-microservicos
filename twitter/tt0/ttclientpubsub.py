#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import zmq

# #  Socket to talk to server
# context = zmq.Context()
# socket = context.socket(zmq.SUB)

# print("Collecting updates from weather server...")
# socket.connect("tcp://localhost:5554")
# followers = ["@greg", "@handboy"]
# followers_filter = ""

# socket.setsockopt_string(zmq.SUBSCRIBE, followers_filter)

# string = socket.recv_string()

# for follow in followers:
#     if string.startswith(follow):
#         print(string)


class ClientPubSub:
    def __init__(self) -> None:
        #  Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        print("Collecting updates from weather server...")
        self.socket.connect("tcp://localhost:5554")
        self.followers = ["@greg", "@handboy"]
        self.followers_filter = ""

    def run(self):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.followers_filter)

        string = self.socket.recv_string()

        for follow in self.followers:
            if string.startswith(follow):
                print(string)
