#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
host = "tcp://localhost:5556"
host = "tcp://0.tcp.sa.ngrok.io:19050"
socket.connect(host)


while True:
    message = input()
    socket.send_string(message)

    reply = socket.recv()
    print(reply)
