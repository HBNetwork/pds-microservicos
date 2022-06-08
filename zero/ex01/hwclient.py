#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import sys
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://0.tcp.sa.ngrok.io:17904")

# python hwclient.py client1 10
name = sys.argv[1]
qty = int(sys.argv[2])

#  Do 10 requests, waiting each time for a response
for request in range(qty):
    print(f"Sending request {request} ...")
    socket.send_string(f"{name}{request}")

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")