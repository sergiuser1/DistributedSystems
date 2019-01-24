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

    print(space.spaces[spaceID]['space'].get(('PING', 2)))
        # print("PING")

def getTest(space, spaceID):
    print(space.spaces[spaceID]['space'].get((str, str, 5)))



space = SequentialSpace()
server = SpaceRepository()
gate = Gate(server, "10.16.161.61", 1242)
server.addSpace("info", space)
server.addGate(gate)
#server.addAgent("info", ping, "info")
#server.addAgent("info", pong, "info")
server.addAgent("info", getTest, "info")
server.start()

while True:
    time.sleep(1.5)
    print("Chat room", server.spaces['info']['space'])
