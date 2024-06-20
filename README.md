# Python函数式的列表与Lambda演算以及Lisp化快速反馈开发

* 如果必要的化引入流行的函数式的库, 或者先用hylang或者libpython-clj来编写,然后GPT翻译python
* 加入Emacs编写各种辅助开发Python体验如Lisp的Elisp

- [x] Emacs集成Python的代码语义搜索
- [ ] Emacs支持GPT从注释输出到函数，以及选中函数翻译目标代码
- [ ] Emacs支持Py的测试自动化开发: 基于xonsh的实现
- [ ] 可以跳转代码，以及搜索所有跳转打开的buffer

---

- [Python函数式的列表与Lambda演算以及Lisp化快速反馈开发](#python%E5%87%BD%E6%95%B0%E5%BC%8F%E7%9A%84%E5%88%97%E8%A1%A8%E4%B8%8Elambda%E6%BC%94%E7%AE%97%E4%BB%A5%E5%8F%8Alisp%E5%8C%96%E5%BF%AB%E9%80%9F%E5%8F%8D%E9%A6%88%E5%BC%80%E5%8F%91)
  - [相关资源](#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%BA%90)
  - [解决import的问题](#%E8%A7%A3%E5%86%B3import%E7%9A%84%E9%97%AE%E9%A2%98)
  - [解决抄Py效率](#%E8%A7%A3%E5%86%B3%E6%8A%84py%E6%95%88%E7%8E%87)
  - [Emacs 开发Elisp，Clojure类似的体验，构建快速纠错反馈循环](#emacs-%E5%BC%80%E5%8F%91elispclojure%E7%B1%BB%E4%BC%BC%E7%9A%84%E4%BD%93%E9%AA%8C%E6%9E%84%E5%BB%BA%E5%BF%AB%E9%80%9F%E7%BA%A0%E9%94%99%E5%8F%8D%E9%A6%88%E5%BE%AA%E7%8E%AF)
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
* [JavaScript函数式的列表](https://github.com/chanshunli/jim-emacs-fun-es6)
* [Functional CSS的列表](https://github.com/chanshunli/jim-emacs-fun-tachyons-flex-css)
* [R function programming list](https://github.com/chanshunli/jim-emacs-fun-r-lisp)

## 解决import的问题
*  独立目录 + `sys.path.append('.')`
```elisp
(defun sys-path-py ()
  (interactive)
  (insert "
import sys
print(sys.path)
print(f\"====Name: {__name__}\")
print(f\"====Package: {__package__}\")
"))
```
## 解决抄Py效率

```elisp
(comment
 (message "1111"))
(defun copy-py-file-by-import2 (start end) ;;=> OK
  ;; (interactive)
  (interactive "r")
  (let* ((file (buffer-substring-no-properties start end))
         (cmd (concat
               "cp /Users/emacspy/Desktop/CxxxyyAIPro111/zzzyyy/zzzyyy/"
               file
               ".py"
               " /Users/emacspy/Desktop/CxxxyyAIPro111/cxxxyy-ai-agent/agenthub/code_agent/")))
    (message "------")
    (message file)
    (message "------")
    (message cmd)
    (shell-command-to-string cmd)))

(defun grep-py-lib (start end)
  (interactive "r")
  (let* ((lib (buffer-substring-no-properties start end))
         (cmd (concat  "cat /Users/emacspy/Desktop/CxxxyyAIPro111/zzzyyy/requirements.txt | grep " lib "| pbcopy"))
         (res (shell-command-to-string cmd)))
    (find-file "/Users/emacspy/Desktop/CxxxyyAIPro111/cxxxyy-ai-agent/pyproject.toml")
    ;; TODO: go chat search march while , do gsub-py-content
    ;; TODO: if no found search the lib in google & open requirements.txt
    (with-current-buffer "pyproject.toml"
      (goto-char (point-max)))
    )
  )

(defun gsub-py-content (start end)
  ;; TODO: 替换py内容
  (interactive "r")
  (let* ((lib (buffer-substring-no-properties start end))
         (cmd (concat "---" lib)))
    (message (shell-command-to-string cmd))
    )
  )

```

## Emacs 开发Elisp，Clojure类似的体验，构建快速纠错反馈循环 
- [ ] 可支持发送函数，语法检查发送整个函数
- [x] 发送行以及实现send-line-to-eshell
- [ ] 发送整个文件`source file.py`，给eshell的ipython的debug 或者是xonsh 
```elisp
;; (+ 1 2) ;; M-x send-region-to-eshell is OK
;; 1 + 2 ; Eshell start ipython is OK, sent code eval ok.
;; TODO: send one line code to ipython
;; TODO: for emacs buffer , send all file content to this eshell buffer
(defun send-region-to-eshell (start end)
  "Send the selected region to Eshell."
  (interactive "r")
  (let ((region (buffer-substring-no-properties start end)))
    (with-current-buffer "*eshell*"
      (goto-char (point-max))
      (insert region)
      (eshell-send-input))))

;; Current GPT Question: in abc.el elisp edit buffer, how to send abc.el currrent line code elisp code to eshell buffer and eval it , and eshell buffer can scroll bottom, and last need cursor gocack abc.el current buffer.
(global-set-key (kbd "C-c e") 'send-line-to-eshell)
;; sid + '------'
(defun send-line-to-eshell ()
  "Take the current line, dispatch it to Eshell, and evaluate there."
  (interactive)
  (let ((code (buffer-substring (line-beginning-position) (line-end-position))))
    (switch-to-buffer-other-window "*eshell*")
    (goto-char (point-max))
    (insert code)
    (eshell-send-input)
    (eshell-scroll-to-bottom)))

;; can not goback
(defun send-line-to-eshell-and-eval ()
  "Send the current line from Emacs buffer to eshell, evaluate it, and return to the origin."
  (interactive)
  (let ((code (thing-at-point 'line t)))
    ;; Open or switch to eshell buffer
    (unless (get-buffer "*esh(ell*")
      (eshell))
    (switch-to-buffer "*eshell*")
    ;; Send the code to eshell
    (goto-char (point-max))
    (insert code)
    (eshell-send-input)
    (eshell-scroll-to-bottom nil nil)
    ;; Return to the original buffer and line
    (switch-to-prev-buffer)
    (back-to-indentation))))

```

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

## test_就是最好的纯函数化的东西

```python
# $ pytest
# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
```

