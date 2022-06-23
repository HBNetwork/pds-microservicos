import zmq

context = zmq.Context()
req = context.socket(zmq.REQ)
req.connect("tcp://localhost:5550")

while True:
    msg = input()
    req.send_string(msg)