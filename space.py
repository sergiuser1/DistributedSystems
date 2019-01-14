
class SequentialSpace:
    def __init__(self):
        self.space = []
        self.types = [str, int, float]

    def __str__(self):
        return str(self.space)

    def put(self, _tuple):
        self.space.append(_tuple)

    def getp(self, _pattern):
        if not any(_type in _pattern for _type in self.types):  # checking for FormalFields
            return self.getp_actual(_pattern)
        else:
            return self.getp_formal(_pattern)

    def getp_actual(self, _pattern):
        if _pattern not in self.space:
            return None
        else:
            for i, element in enumerate(self.space):
                if element == _pattern:
                    return self.space.pop(i)

    def getp_formal(self, _pattern):
        for i, element in enumerate(self.space):
            satisfy = True
            for j, field in enumerate(_pattern): # checking each tuple element by element
                if type(field) == type: # if it's a formal field
                    if j < len(element) and type(element[j]) != _pattern[j]:
                        satisfy = False
                else:                   # if it's an actual field
                    if j < len(element) and element[j] != _pattern[j]:
                        satisfy = False
            if satisfy:
                return self.space.pop(i)

        return None

    def queryp(self, _pattern):
        if not any(_type in _pattern for _type in self.types):
            return self.queryp_actual(_pattern)
        else:
            return self.queryp_formal(_pattern)

    def queryp_actual(self, _pattern):
        if _pattern not in self.space:
            return None
        else:
            for i, element in enumerate(self.space):
                if element == _pattern:
                    return element

    # TODO change so it only returns iff all the conditions are satisfied
    def queryp_formal(self, _pattern):
        for i, element in enumerate(self.space):
            satisfy = True
            for j, field in enumerate(_pattern):
                if type(field) == type:
                    if j < len(element) and type(element[j]) != _pattern[j]:
                        satisfy = False
                else:
                    if j < len(element) and element[j] != _pattern[j]:
                        satisfy = False
            if satisfy:
                return element

        return None

# tests
space = SequentialSpace()
space.put(("coffee", 1))
space.put(("kitchen",))
space.put(("coffee", 2))

print(space)
print(space.getp((str, )))
print(space)
print(space.queryp((str, 3)))
print(space)
