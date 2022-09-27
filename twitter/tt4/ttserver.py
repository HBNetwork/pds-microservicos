import time

import zmq


def server(commands):
    context = zmq.Context()
    rep = context.socket(zmq.REP)
    rep.bind("tcp://*:5557")

    pub = context.socket(zmq.PUB)
    pub.bind("tcp://*:5554")

    while True:
        #  Wait for next request from client
        message = rep.recv()

        #print(f"SERVER: Received request: {message}")

        reply = "\n"

        try:
            cmd, user, *arg = message.decode("utf-8").split(" ", maxsplit=2)
            reply = commands(cmd, user, *arg)
            #print(reply)

            if cmd == "tweet":
                pub.send_string(f"@{user} {message}")
            elif cmd == "followers":
                reply = ",".join(reply) if reply else ""
        except Exception as e:
            reply = f"ERRO: {str(e)}"

        rep.send_string(reply)

        #time.sleep(0.01)



if __name__ == "__main__":
    from core import commands
    try:
        server(commands)
    except KeyboardInterrupt:
        pass
