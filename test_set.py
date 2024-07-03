
files = ["aaa.py", "baa.py"]

set(files) #=> {'aaa.py', 'baa.py'}

for file in set(files):
    print(file)

set(files)[0] #=> TypeError: 'set' object is not subscriptable

set(files).pop() #=> aaa.py

if len(set('111')) > 0:
    print(111)

sett = set('dsadsa')

len(sett) ? sett : ""

list(sett)

set().pop()
