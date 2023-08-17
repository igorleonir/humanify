import zmq
import json
from rename import rename

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("ipc:///tmp/humanify-local-inference-server.ipc")

print("Server started")

while True:
    # JSON parse the message
    message = json.loads(socket.recv())

    before = message['before']
    after = message['after']

    renamed = rename(before, after)

    # Send reply back to client
    socket.send_string(json.dumps({"type": "renamed", "renamed": renamed}))