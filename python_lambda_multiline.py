#!/usr/bin/python
#-*-coding:utf-8 -*-
aaa = lambda a,b: (
    a*b
    )
#print aaa(5,2) #=> 10
# 这里面不能用等号赋值表达式==>
aaa1 = lambda a,b: (
    a,
    b,
    a+b,
    a*b,
    a-b
    )
# 输出是一个列表来着:
#print aaa1(222,110) #=> (222, 110, 332, 24420, 112)

aaa2 = lambda a,b: (
    a,
    b,
    a+b,
    a*b,
    a-b
    )[-1]
# [-1] 是输出最后一个答案的意思
# print aaa2(222,110) #=> 112 

# 在lambda中运行这三个运算: 只能变成数组去 pop 取出, append 加入来运算了 # 因为不能进行赋值操作(SyntaxError: can't assign to lambda)
# a = a + b
# b = b * c;
# return a + b + c;
aaa3 = lambda a,b,c: (
    a.append(a.pop() + b[-1]),
    b.append(b.pop() * c),
    a[-1] + b[-1] + c
    )
# print aaa3([1],[2],1) #=> (None, None, 6)
# print aaa3([1],[2],1)[-1] #=> 6

#aaa4 = lambda a,b,c: a+b+c,a #=> NameError: name 'a' is not defined
#aaa4 = lambda a,b,c: (a+b+c,a) #=> ok
#aaa4 = lambda a,b,c: a+b+c;a #=> NameError: name 'a' is not defined
