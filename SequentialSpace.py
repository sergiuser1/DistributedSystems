import threading
from threading import Condition, Lock
from queue import Queue

class SequentialSpace:
    def __init__(self):
        self.space = []
        self.types = [str, int, float]
        self.editor_lock = Condition(lock=Lock())
        self.query_lock = Condition(lock = Lock())
        self.reader_count = 0

    def __str__(self):
        return str(self.space)

    def put(self, _tuple):
        print("im puttimh")
        with self.editor_lock, self.query_lock:
            self.space.append(_tuple)
            self.query_lock.notify_all()
            self.editor_lock.notify_all()

    def getp(self, _pattern):
        with self.editor_lock, self.query_lock:
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
        print('stuck')
        with self.editor_lock:
            satisfy = False
            while not satisfy:
                if not any(_type in _pattern for _type in self.types):  # checking for FormalFields
                    if _pattern not in self.space:
                        self.editor_lock.wait()
                        print("Formal Search wait")
                    else:
                        satisfy = True
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
                        else:
                            self.editor_lock.wait()
                            print("Actual Search wait")

    def queryp(self, _pattern):
        self.reader_count += 1
        if self.reader_count == 1:
            with self.query_lock:
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
        with self.editor_lock, self.reader_condition:
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
        with self.writer_condition and self.reader_condition:
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

space.put(("kitchen",))
space.put(("another", 2, 3))
space.put(("last", 1.5))
space.put((122, 12.5, "q2q3"))

def wrapper(func, arg, queue):
    return queue.put(func(arg))


q1, q2, q3 = Queue(), Queue(), Queue()
tup1 = ("coffee", int)
tup2 = ("coffee",1)
a =threading.Thread(target= wrapper, args=(space.get,tup1,q1))
b=threading.Thread(target= wrapper, args=(space.put,tup2,q1))
c=threading.Thread(target= wrapper, args=(space.put,tup2,q1))
a.start()
b.start()
c.start()
print(threading.active_count())
a.join()
b.join()
c.join()
print(threading.active_count())
#print(space.queryAll((str, )))
print(space)