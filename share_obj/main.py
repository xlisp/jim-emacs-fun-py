# main.py

from singleton import Singleton

obj = Singleton.get_instance()
obj.display()

obj.value = 200  # Update the value

