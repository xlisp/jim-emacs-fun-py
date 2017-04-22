### jim-emacs-fun-py python函数式的列表(如果必要的化引入流行的函数式的库)
* `M-x py-utf-8`
```emacs-lisp
(defun py-utf-8 ()
  (interactive)
  (insert "#!/usr/bin/python\n#-*-coding:utf-8 -*-\n")
  )
```
* lambda [多行的lambda使用](./python_lambda_multiline.py)
```py
add = lambda a,b : a + b
print add(2,3)
# or 
(lambda a,b : a + b)(2,3)
```
* map
```py
map(len,['aaa','faag','stevech']) #=> [3, 4, 7]
```
* each 
```py
list(len(s) for s in ['sentence', 'fragment']) #=> [8, 8]
#
abc = ['aaa','faag','stevech']
for i in range(len(abc)):
    print len(abc[i])

#====> enumerate 是取key和index
for index, key in enumerate({'aaa' : 1111, 'bbb' : 222}):
    print key, index
# aaa 0
# bbb 1    

#====> iteritems 是取key和val
# For Python 3.x: for key, val in d.items():
for key, val in {'aaa' : 1111, 'bbb' : 222}.iteritems():
    print key, val
#  aaa 1111
#  bbb 222

```
* reduce
```py
reduce(lambda a,b : a + b,[2,3,4]) #=> 9
reduce(lambda a,b: a+b, [1,2,3,4], 100) #=> 110

# 
reduce(lambda su,key: key + su, vaAAs, [])

# ====>>> for 版本
ooo = []
for va in vaAAs:
    ooo = va + ooo

```
* filter
```py
filter(lambda x: x>0, [2, -5, 9, -7, 2, 5, 4, -1, 0, -3, 8]) #=> [2, 9, 2, 5, 4, 8]
# => or 方法必须要return布尔值, py的lambda替换为def函数要return
def myfn(x, y):
    if x > 0:
        return True
    else:
        return False

filter(lambda x: myfn(x, 222), [2, -5, 9, -7, 2, 5, 4, -1, 0, -3, 8]) #=> [2, 9, 2, 5, 4, 8]
```
* yield
```py
def aaa(a):
    yield a
next(aaa(1)) #=> 1
```
* sorted
```py
# 默认是从小到大排序: ` lambda a,b: a-b `
sorted([769, 2207, 6213, 6431, 7953, 8442, 9828, 9878], lambda a,b: b-a) #=> [9878, 9828, 8442, 7953, 6431, 6213, 2207, 769]
```

* flatten (只有Numpy提供)

```py
import numpy as np
a = [[1,3],[2,4],[3,5]]
a = np.array(a)
a.flatten() #=> array([1, 3, 2, 4, 3, 5])

```
* combinations and permutations (只有itertools提供组合和排列的方法)

```py
from itertools import *
list(combinations([1, 2, 11, 12, 21, 22], 3))
#=> [(1, 2, 11), (1, 2, 12), (1, 2, 21), (1, 2, 22), (1, 11, 12), (1, 11, 21), (1, 11, 22), (1, 12, 21), (1, 12, 22), (1, 21, 22), (2, 11, 12), (2, 11, 21), (2, 11, 22), (2, 12, 21), (2, 12, 22), (2, 21, 22), (11, 12, 21), (11, 12, 22), (11, 21, 22), (12, 21, 22)]
```
* partial (只有functools有)
```py
import functools
def abc(a, b):
    print a, b
functools.partial(abc, 111)(222) #=> 111 222
```
* apply 
```py
apply(lambda a,b: a+b, [1, 2]) #=> 3
apply(lambda a, b, c, d: a + b + c + d, [[1], [2], [3], [5, 6, 7]]) #=> [1, 2, 3, 5, 6, 7]
```
