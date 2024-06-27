from abc import ABC

# https://docs.python.org/zh-cn/3.10/library/abc.html
# 将“子类”注册为该抽象基类的“抽象子类”，例如：

class MyABC(ABC):
    pass

MyABC.register(tuple)

#print( issubclass(tuple, MyABC)) #=> True
#print( isinstance((), MyABC)) #=> True

## =>https://www.cnblogs.com/marsggbo/p/12119370.html　　抽象类是一个特殊的类，只能被继承，不能实例化
import abc  # 利用abc模块实现抽象类

class File(metaclass=abc.ABCMeta):  # abc.ABCMeta是实现抽象类的一个基础类
    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def read(self):
        pass

class Txt(File):  # 子类继承抽象类，但是必须定义read方法将抽象类中的read方法覆盖
    def read(self):
        print('文本数据的读取方法')

txt1 = Txt()
txt1.read() #=> 文本数据的读取方法
#txt2 = File() # TypeError: Can't instantiate abstract class File with abstract method read
#txt2.read()
