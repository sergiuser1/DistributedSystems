
class SequentialSpace:
    def __init__(self):
        self.space = []

    def put(self, _tuple):
        self.space.append(_tuple)

    def queryp(self, _tuple):
        if _tuple not in self.space:
            return None
        else:
            for element in self.space:
                if element == _tuple:
                    return element

    def getp(self, _tuple):
        if _tuple not in self.space:
            return None
        else:
            for i, element in enumerate(self.space):
                if element == _tuple:
                    return self.space.pop(i)
