import socket
import threading
import time
from pySpace.gate import sendJson, receiveJson


jackHost = "10.16.108.101"
jackPort = 12123

request = {
            "action": "PUT_REQUEST",
            "source" : ("10.16.108.101", 12123),
            "target": 'info',
            "tuple" : ('Jack says hi', 1) }


def trySend(host, port, dict):

    while True:
        time.sleep(1)
        try:
            sendJson(host, port, dict)
            break
        except:
            print("Send didn't work, trying again in one second")

host = "10.16.161.61"
port = 1242

trySend(host, port, request)
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the socket
s.bind((host, port))
s.listen(1)
connection, address = s.accept()

data = receiveJson(connection)

print(data['ee'])
"""



# 100 = writers queue is full
# 0 = ok

