# jim-emacs-fun-py python函数式的列表(如果必要的化引入流行的函数式的库, 或者先用hylang来编写,然后编译为python)

- [jim-emacs-fun-py python函数式的列表(如果必要的化引入流行的函数式的库, 或者先用hylang来编写,然后编译为python)](#jim-emacs-fun-py-python%E5%87%BD%E6%95%B0%E5%BC%8F%E7%9A%84%E5%88%97%E8%A1%A8%E5%A6%82%E6%9E%9C%E5%BF%85%E8%A6%81%E7%9A%84%E5%8C%96%E5%BC%95%E5%85%A5%E6%B5%81%E8%A1%8C%E7%9A%84%E5%87%BD%E6%95%B0%E5%BC%8F%E7%9A%84%E5%BA%93-%E6%88%96%E8%80%85%E5%85%88%E7%94%A8hylang%E6%9D%A5%E7%BC%96%E5%86%99%E7%84%B6%E5%90%8E%E7%BC%96%E8%AF%91%E4%B8%BApython)
  - [相关资源](#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%BA%90)
    - [JavaScript函数式的列表](#javascript%E5%87%BD%E6%95%B0%E5%BC%8F%E7%9A%84%E5%88%97%E8%A1%A8)
    - [Functional CSS的列表](#functional-css%E7%9A%84%E5%88%97%E8%A1%A8)
  - [`M-x py-utf-8`](#m-x-py-utf-8)
  - [lambda 多行的lambda使用](#lambda-%E5%A4%9A%E8%A1%8C%E7%9A%84lambda%E4%BD%BF%E7%94%A8)
  - [map](#map)
  - [each](#each)
  - [reduce](#reduce)
  - [filter](#filter)
  - [yield](#yield)
  - [sorted](#sorted)
  - [flatten (只有Numpy提供)](#flatten-%E5%8F%AA%E6%9C%89numpy%E6%8F%90%E4%BE%9B)
  - [combinations and permutations (只有itertools提供组合和排列的方法)](#combinations-and-permutations-%E5%8F%AA%E6%9C%89itertools%E6%8F%90%E4%BE%9B%E7%BB%84%E5%90%88%E5%92%8C%E6%8E%92%E5%88%97%E7%9A%84%E6%96%B9%E6%B3%95)
  - [partial (只有functools有)](#partial-%E5%8F%AA%E6%9C%89functools%E6%9C%89)
  - [apply](#apply)
  - [Math Combinatorics: cartesian product](#math-combinatorics-cartesian-product)
  - [clojure for in py](#clojure-for-in-py)

## 相关资源
### [JavaScript函数式的列表](https://github.com/chanshunli/jim-emacs-fun-es6)
### [Functional CSS的列表](https://github.com/chanshunli/jim-emacs-fun-tachyons-flex-css)

## `M-x py-utf-8`
```emacs-lisp
(defun py-utf-8 ()
  (interactive)
  (insert "#!/usr/bin/python\n#-*-coding:utf-8 -*-\n")
  )
```
## lambda [多行的lambda使用](./python_lambda_multiline.py)
```py
add = lambda a,b : a + b
print add(2,3)
# or
(lambda a,b : a + b)(2,3)
```
## map
```py
map(len,['aaa','faag','stevech']) #=> [3, 4, 7]
```
## each
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
## reduce
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
## filter
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
## yield
```py
def aaa(a):
    yield a
next(aaa(1)) #=> 1
```
## sorted
```py
# 默认是从小到大排序: ` lambda a,b: a-b `
sorted([769, 2207, 6213, 6431, 7953, 8442, 9828, 9878], lambda a,b: b-a) #=> [9878, 9828, 8442, 7953, 6431, 6213, 2207, 769]
```

## flatten (只有Numpy提供)

```py
import numpy as np
a = [[1,3],[2,4],[3,5]]
a = np.array(a)
a.flatten() #=> array([1, 3, 2, 4, 3, 5])

```
## combinations and permutations (只有itertools提供组合和排列的方法)

```py
from itertools import *
list(combinations([1, 2, 11, 12, 21, 22], 3))
#=> [(1, 2, 11), (1, 2, 12), (1, 2, 21), (1, 2, 22), (1, 11, 12), (1, 11, 21), (1, 11, 22), (1, 12, 21), (1, 12, 22), (1, 21, 22), (2, 11, 12), (2, 11, 21), (2, 11, 22), (2, 12, 21), (2, 12, 22), (2, 21, 22), (11, 12, 21), (11, 12, 22), (11, 21, 22), (12, 21, 22)]
```
## partial (只有functools有)
```py
import functools
def abc(a, b):
    print a, b
functools.partial(abc, 111)(222) #=> 111 222
```
## apply
```py
apply(lambda a,b: a+b, [1, 2]) #=> 3
apply(lambda a, b, c, d: a + b + c + d, [[1], [2], [3], [5, 6, 7]]) #=> [1, 2, 3, 5, 6, 7]
```
## Math Combinatorics: cartesian product

```py
import itertools
somelists = [
    [1, 2, 3],
    ['a', 'b'],
    [4, 5]
]

[element for element in itertools.product(*somelists)] # 12种组合
#=> [(1, 'a', 4), (1, 'a', 5), (1, 'b', 4) ... ]
```
## clojure for in py
```py

[(a, b, c) for a in [1,2,3] for b in ['a','b'] for c in [4,5]]
#=>
[(1, 'a', 4), (1, 'a', 5), (1, 'b', 4), (1, 'b', 5), (2, 'a', 4),
 (2, 'a', 5), (2, 'b', 4), (2, 'b', 5), (3, 'a', 4), (3, 'a', 5),
 (3, 'b', 4), (3, 'b', 5)]
```
```clojure
(for [a  [1 2 3] b  ["a" "b"] c  [4 5]] [a b c])
;; => ([1 "a" 4] [1 "a" 5] [1 "b" 4] [1 "b" 5] [2 "a" 4] [2 "a" 5] [2 "b" 4] [2 "b" 5] [3 "a" 4] [3 "a" 5] [3 "b" 4] [3 "b" 5])

```
