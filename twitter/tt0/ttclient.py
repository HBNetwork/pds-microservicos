#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

# context = zmq.Context()

# #  Socket to talk to server
# print("Connecting to hello world server...")
# socket = context.socket(zmq.REQ)
# host = "tcp://localhost:5557"
# #host = "tcp://0.tcp.sa.ngrok.io:19050"
# socket.connect(host)


# while True:
#     message = input()
#     socket.send_string(message)

#     reply = socket.recv()
#     print("SERVER RESPONSE: ", reply)


class Client:
    def __init__(self) -> None:
        self.context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to hello world server...")
        self.socket = self.context.socket(zmq.REQ)
        self.host = "tcp://localhost:5557"
        # host = "tcp://0.tcp.sa.ngrok.io:19050"
        self.socket.connect(self.host)

    def run(self):
        while True:
            # Send command to server
            message = input()
            self.socket.send_string(message)
            reply = self.socket.recv()
            print("SERVER RESPONSE: ", reply)

            # Recebe os tweets da galera
            # self.client_pubsub.run()
    
    def signup(self, username):
        self.socket.send_string(f'signup {username}')
        return self.socket.recv()
    
    def followers(self, username):
        self.socket.send_string(f'followers {username}')
        return self.socket.recv()


if __name__ == "__main__":
    server = Client()
    server.run()
