import threading



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


