from space import SequentialSpace
from network import Gate, sendJson
import threading
import time


class SpaceRepository:

    def __init__(self):
        self.spaces = {} # a space is identified by its spaceID, and it contains the space itself
        self.gates = []  # as well as the agents associated to it

    def addSpace(self, spaceId, space):
        if spaceId in self.spaces:
            raise AttributeError
        else:
            self.spaces[spaceId] = {'space':space,
                                    'agents':[]}

    def delSpace(self, spaceId):
        if spaceId not in self.spaces:
            return False
        else:
            self.spaces.pop(spaceId)
            return True

    def addGate(self, gate):
        if gate in self.gates:
            return False
        else:
            self.gates.append(gate)
            return True

    def closeGate(self, gate):
        if gate not in self.gates:
            return False
        else:
            self.gates.remove(gate)

    def addAgent(self, spaceId, agent, *agent_args):
        agent_args = (self,) + agent_args
        thread = threading.Thread(target=agent, args=agent_args)
       # thread.daemon = True # ensuring the threads stop when the main is stopped
        self.spaces[spaceId]['agents'].append(thread)

    def start(self):
        for gate in self.gates:
            gate.start()

        for key in self.spaces:
            for thread in self.spaces[key]['agents']:
                thread.start()


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
            "source" : ("127.0.0.1", 31415),
            "target": 'info',
            "tuple" : ('PING', -4) }

request2 = {
            "action": "GETP_REQUEST",
            "source" : ("127.0.0.1", 31415),
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
