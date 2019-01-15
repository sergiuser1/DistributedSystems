class Tuples:
    def __init__(self,*arg):
        self.Tuple = tuple(list(arg))

    def __str__(self):
        return str(self.Tuple)

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        if self.index == len(self.Tuple)-1:
            raise StopIteration
        self.index += 1
        return self.Tuple[self.index]

    def GetFieldAt(self,index):
        return list(self)[index]


a = Tuples(1,2,3,"hello",(1,2))


print(a)
print(a.GetFieldAt(4))

"""def tuple_create(*arg):
        tlist = []
        for item in arg:
            tlist.append(item)
        finaltuple = tuple(tlist)
        return finaltuple

a = ('2',)
b = ('z',3,"hello")
new = a + (b,)
print(tuple("a",2,("hello", 3))) """
