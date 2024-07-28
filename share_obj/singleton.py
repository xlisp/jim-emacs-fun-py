class MyObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def display(self):
        print(f"Name: {self.name}, Value: {self.value}")

class Singleton:
    _instance = None

    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            Singleton._instance = MyObject("SharedObject", 100)
        return Singleton._instance

