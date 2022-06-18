#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq

# context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5554")

# while True:
#     topic = "twitter2"
#     user = "greg"
#     message = "Olas"

#     socket.send_string(f"@{user} {message}")
#     socket.send_string(f"@handboy {message}")


class ServerPubSub:
    def __init__(self) -> None:
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5554")

    def send_tweet(self, user, message):
        print("ENVIANDO TWEET: ", message)
        self.socket.send_string(f'@{user} {message}')
