## https://python.plainenglish.io/better-python-singleton-with-a-metaclass-41fb8bfe2127

from shape import make_new_shape

class MyShape:
    shaper = None  # we can store the value as a class variable

    # we could also store the value as an instance variable.
    # it makes no difference - the shape will only ever be set once.

    def __init__(self, s):
        MyShape.shaper = make_new_shape(s)

    def get(self):
        return MyShape.shaper

x = MyShape("square")
y = MyShape("circle")
print(f"x is {x.get()}  y is {y.get()}")
# => # that prints x is square   y is square
