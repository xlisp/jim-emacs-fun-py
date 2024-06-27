
def make_new_shape(s):
  global shape
  if shape is None:
    # you can only make new shape (and set the value) once.
    shape = s
  return shape

__all__ = [make_new_shape]

shape = None
