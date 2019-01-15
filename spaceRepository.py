from space import SequentialSpace

class SpaceRepository:

    def __init__(self):
        self.spaces = {}
        self.gates = []

    def addSpace(self, spaceId, space):
        if spaceId in self.spaces:
            raise AttributeError
        else:
            self.spaces[spaceId] = space

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