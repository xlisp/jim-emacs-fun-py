# another_file.py

from singleton import Singleton

obj = Singleton.get_instance()
obj.display()  # This will display the updated value 200
