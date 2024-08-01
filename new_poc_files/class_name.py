import unittest

class MyClass:
    def get_class_name(self):
        return self.__class__.__name__

class TestMyClass(unittest.TestCase):
    def test_get_class_name(self):
        obj = MyClass()
        self.assertEqual(obj.get_class_name(), 'MyClass')

if __name__ == '__main__':
    unittest.main()