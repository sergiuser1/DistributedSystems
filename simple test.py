from pySpace.spaceRepository import SpaceRepository
from pySpace.gate import Gate, sendJson, receiveJson
from pySpace.sequentialSpace import SequentialSpace
import time


def ping(space, spaceID):
    for i in range(10):
        time.sleep(1)
        space.spaces[spaceID]['space'].put(("PING", i))
       # print("ping is", space.spaces[spaceID]['space'])
        #print("PING")


def pong(space, spaceID):
    for i in range(10):
        time.sleep(1.1)
        print(space.spaces[spaceID]['space'].getp(("PING", i)))
        # print("PING")


request = {
            "action": "PUT_REQUEST",
            "source" : ("127.0.0.1", 12123),
            "target": 'info',
            "tuple" : ('PING', -4) }

request2 = {
            "action": "GETP_REQUEST",
            "source" : ("127.0.0.1", 12312),
            "target": 'info',
            "tuple" : ('PING', -1) }

space = SequentialSpace()
server = SpaceRepository()
gate = Gate(server, "127.0.0.1")
server.addSpace("info", space)
server.addGate(gate)
server.addAgent("info", ping, "info")
server.addAgent("info", pong, "info")
server.start()
sendJson('127.0.0.1', 31415, request)
print("server is", server.spaces['info']['space'])
time.sleep(1)
sendJson('127.0.0.1', 31415, request2)

while True:
    time.sleep(0.5)
    print("server is", server.spaces['info']['space'])
