from queue import Queue

def add(x,y):
    print(x+y)

temp = Queue()

temp.put([[2,3], lambda x,y: add(x,y)])
print('asdf')
stuff = temp.get()
stuff[1](stuff[0][0], stuff[0][1])
print((temp.empty()))