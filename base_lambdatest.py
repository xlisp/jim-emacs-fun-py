num = 52
if num == 3:
    print('111')
elif num == 5:
    print('222')
else: # 不一定需要带else结尾
    print(333)

print("Google" in set(("Google", "Runoob", "Taobao")))

def abc():
    a = ""
    # 这个相当于lambda的存在，但是不能带入局部变量
    def append(str):
        a = a + str
    append("1111")
    append("11112222")
    return a
# UnboundLocalError: cannot access local variable 'a' where it is not associated with a value
# print(abc())

b = ""
def abc1():
    # 这个相当于lambda的存在，但是不能带入局部变量
    def append(str):
        b = b + str
    append("1111")
    append("11112222")
    return b
#UnboundLocalError: cannot access local variable 'b' where it is not associated with a value
#print(abc1())

class Abcd:
    def __init__(self, a):
        self.a = ""

    def abc(self):
        def append(str):
            self.a = self.a + str
        append("1111")
        append("11112222")
        return self.a

c = Abcd("===")
print(c.abc()) #111111112222

def abc3():
    a = "--"
    # 这个相当于lambda的存在，但是不能带入局部变量
    #append = lambda str: a = a + str # => SyntaxError: cannot assign to lambda
    append = lambda str: a + str
    append("1111333")
    append("11112222333")
    return a

print(abc3()) #=> --

def abc5():
    a = "--"
    # 这个相当于lambda的存在，但是不能带入局部变量
    #append = lambda str: a = a + str # => SyntaxError: cannot assign to lambda
    append = lambda str: a + str
    #append("1111333")
    #append("11112222333")
    return append(append("1111333"))

print(abc5()) #=>
# ----1111333
