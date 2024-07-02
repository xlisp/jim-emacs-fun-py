#--- https://fantasyhh.github.io/2020/01/12/python-yield-from/
def chain(*iterables):
    for it in iterables:
        for i in it:
            yield i

s = 'ABC'
t = tuple(range(3))
list(chain(s, t)) #=> ['A', 'B', 'C', 0, 1, 2]

## ----- 把for迭代器向后传递出去

def chain2(*iterables):
    for i in iterables:
        yield from i

chain2(s, t) #=> <generator object chain2 at 0x103749f20>

list(chain2(s, t))
# ['A', 'B', 'C', 0, 1, 2]
