
class SequentialSpace:
    def __init__(self):
        self.space = []
        self.types = [str, int, float]

    def __str__(self):
        return str(self.space)

    def put(self, _tuple):
        self.space.append(_tuple)

    def getp(self, _pattern, nonBlocking=True):
        if not any(_type in _pattern for _type in self.types):  # checking for FormalFields
            if _pattern not in self.space:
                return None
            else:
                for i, element in enumerate(self.space):
                    if element == _pattern:
                        return self.space.pop(i)
        else:
            for i, element in enumerate(self.space):
                satisfy = True
                for j, field in enumerate(_pattern):  # checking each tuple element by element
                    if type(field) == type:  # if it's a formal field
                        if j < len(element) and type(element[j]) != _pattern[j]:
                            satisfy = False
                    else:                   # if it's an actual field
                        if j < len(element) and element[j] != _pattern[j]:
                            satisfy = False
                if satisfy:
                    return self.space.pop(i)

            return None

    # blocking get
    def get(self, _pattern):
        while True:
            if not any(_type in _pattern for _type in self.types):  # checking for FormalFields
                if _pattern not in self.space:
                    pass
                else:
                    for i, element in enumerate(self.space):
                        if element == _pattern:
                            return self.space.pop(i)
            else:
                for i, element in enumerate(self.space):
                    satisfy = True
                    for j, field in enumerate(_pattern):  # checking each tuple element by element
                        if type(field) == type:  # if it's a formal field
                            if j < len(element) and type(element[j]) != _pattern[j]:
                                satisfy = False
                        else:                   # if it's an actual field
                            if j < len(element) and element[j] != _pattern[j]:
                                satisfy = False
                    if satisfy:
                        return self.space.pop(i)



    def queryp(self, _pattern):
        if not any(_type in _pattern for _type in self.types):
            if _pattern not in self.space:
                return None
            else:
                for i, element in enumerate(self.space):
                    if element == _pattern:
                        return element
        else:
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


    def query(self, _pattern):
        while True:
            if not any(_type in _pattern for _type in self.types):
                if _pattern not in self.space:
                    pass
                else:
                    for i, element in enumerate(self.space):
                        if element == _pattern:
                            return element
            else:
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


    # getAll
    def getAll(self, _pattern):
        if not any(_type in _pattern for _type in self.types):
            if _pattern not in self.space:
                return None
            else:
                elements = []
                for i, element in enumerate(self.space):
                    if element == _pattern:
                        elements.append(self.space.pop(i))
                return elements
        else:
            elements = []
            i = 0
            while i < len(self.space):
                element = self.space[i]
                satisfy = True
                for j, field in enumerate(_pattern):  # checking each tuple element by element
                    if type(field) == type:  # if it's a formal field
                        if j < len(element) and type(element[j]) != _pattern[j]:
                            satisfy = False
                    else:  # if it's an actual field
                        if j < len(element) and element[j] != _pattern[j]:
                            satisfy = False
                if satisfy:
                    elements.append(self.space.pop(i))
                    i -= 1
                i += 1
            return elements


    # queryAll
    def queryAll(self, _pattern):
        if not any(_type in _pattern for _type in self.types):
            if _pattern not in self.space:
                return None
            else:
                elements = []
                for i, element in enumerate(self.space):
                    if element == _pattern:
                        elements.append(element)
                return elements
        else:
            elements = []
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
                    elements.append(element)

            return elements

# tests

space = SequentialSpace()
space.put(("coffee", 1))
space.put(("kitchen",))
space.put(("coffee", 2))
space.put(("another", 2, 3))
space.put(("last", 1.5))

print(space)
print(space.get((str,)))
print(space)
print(space.queryAll((str, )))
print(space)
