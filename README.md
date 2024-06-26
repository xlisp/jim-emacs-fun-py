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
  - [test_就是最好的纯函数化的东西](#test_%E5%B0%B1%E6%98%AF%E6%9C%80%E5%A5%BD%E7%9A%84%E7%BA%AF%E5%87%BD%E6%95%B0%E5%8C%96%E7%9A%84%E4%B8%9C%E8%A5%BF)
  - [Python async await](#python-async-await)
  - [Python单文件执行快速验证概念](#python%E5%8D%95%E6%96%87%E4%BB%B6%E6%89%A7%E8%A1%8C%E5%BF%AB%E9%80%9F%E9%AA%8C%E8%AF%81%E6%A6%82%E5%BF%B5)
  - [Python remote repl for debug不要在线上编程](#python-remote-repl-for-debug%E4%B8%8D%E8%A6%81%E5%9C%A8%E7%BA%BF%E4%B8%8A%E7%BC%96%E7%A8%8B)
  - [Emacs yasnippet帮助快速写脚手架代码, 算法脚手架](#emacs-yasnippet%E5%B8%AE%E5%8A%A9%E5%BF%AB%E9%80%9F%E5%86%99%E8%84%9A%E6%89%8B%E6%9E%B6%E4%BB%A3%E7%A0%81-%E7%AE%97%E6%B3%95%E8%84%9A%E6%89%8B%E6%9E%B6)
  - [Python lambda演算](#python-lambda%E6%BC%94%E7%AE%97)

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
* https://github.com/apachecn/zetcode-zh/blob/master/docs/py/39.md
```bash
## 测试特定文件
$ pytest  tests/test_min_max_test.py # TODO：Emacs 开发一个C-c C-k，找到对应的测试文件是谁

## 测试特定的函数 => TODO: Emacs开发一个插件，向上寻找当前函数名，C-c C-c发送给执行文件, 用ast的库实现.
$ pytest  tests/test_min_max_test.py::test_min

```

## Python async await
* ^^ 原则：发现是一个阻塞操作, 就新建一个async协程对象, 当队列来处理，然后队列里面需要做一个'callback'操作队列的单个元素-处理队的操作: 通常再定义一个async函数去await处理它如`async def ws_send(word)`  ^^
*  async协程对象对象里面可以包含async，是递归的, await只能调用async定义的方法
* https://martinxpn.medium.com/async-await-in-python-asyncio-deep-dive-76-100-days-of-python-31b44cb28d82
*  如果一个函数有阻塞操作，如time.sleep(1) , 就需要头部加上`async def xxx`, 然后阻塞的地方加上`await asyncio.sleep` or `await litellm.acompletion(..)` 
*  如果函数里面还有多个的阻塞操作：也需要新建一个async协程对象 `async with aiohttp.ClientSession()`, 然后await其结果`await fetch_html(session, url)`
*  或者是一个"流队列对象"，也可以新建一个async协程对象`async for chunk in llm_response:`, 然后await其结果`await ws_send_msg(word)`
* await 只能在async函数里面去使用：`SyntaxError: 'await' outside async function`, 而且只能await调用coroutine对象或者是async函数
```python
坚持去λ化(中-易) ~  @ async def hello_world():
.....................     print('Hello')
.....................     await asyncio.sleep(1)
.....................     print('World')
.....................
坚持去λ化(中-易) ~  @ hello_world()
<coroutine object hello_world at 0x107851a80> ##=> 协程是一个对象，不能直接运行
坚持去λ化(中-易) ~  @ asyncio.run(hello_world())
Hello
World
坚持去λ化(中-易) ~  @
```
* Event loops
```python
import asyncio
async def my_coroutine():
    print('Coroutine started')
    await asyncio.sleep(1)
    print('Coroutine finished')
loop = asyncio.get_event_loop()
loop.run_until_complete(my_coroutine())
loop.close()
# Coroutine started
# Coroutine finished
```
* Task
```python
async def my_coroutine():
    print('Coroutine started')
    await asyncio.sleep(1)
    print('Coroutine finished')
async def main():
    task = asyncio.create_task(my_coroutine())
    await task
asyncio.run(main())
```
* https://www.cnblogs.com/yoyoketang/p/16256696.html Old version
```bash
python async_test.py
python async_test2.py
python await_test.py
```
* [llm stream](./llm_stream.py)
```python
import litellm
import asyncio

from litellm import acompletion

async def test_get_response_stream(q):
    user_message = q #"Hello, how are you?"
    messages = [{"content": user_message, "role": "user"}]
    response = await acompletion(model="gpt-3.5-turbo", messages=messages, stream=True)
    # return response
    res = ''
    async def ws_send(word):
        # await print(word) ## 只能await async过来的对象：TypeError: object NoneType can't be used in 'await' expression
        print(word)
    # for chunk in response: ## 无法直接取出，是一个队列对象，TypeError: 'AsyncStream' object is not an iterator
    async for chunk in response:
        word = chunk.choices[0].delta.content or ''
        res = res + word
        #await print(word, end='', flush=True) ## TypeError: object NoneType can't be used in 'await' expression
        await ws_send(res)

asyncio.run(test_get_response_stream("hi"))
# => 
# Hello
# Hello!
# Hello! How
# Hello! How can
# Hello! How can I
# Hello! How can I assist
# Hello! How can I assist you
# Hello! How can I assist you today
# Hello! How can I assist you today?
# Hello! How can I assist you today?
```
* Asyncio Queue: like clojure async pub sub
- [POC: clojure pub sub log](./src/system_principles/clojure_async_2chan_log.clj)

```python
import asyncio
from asyncio import Queue

async def log_scribe():
    a = Queue()  # Our channel A, the log's main door

    async def logging_loop():
        while True:
            msg = await a.get()
            if msg is None:
                break
            print("Logging:", msg)

    asyncio.create_task(logging_loop())
    return a

async def log_listener(a):
    b = Queue()  # Channel B, to hear and see

    async def listener_loop():
        while True:
            msg = await b.get()
            if msg is None:
                break
            print("Listener:", msg)

    async def forward_logs():
        while True:
            msg = await a.get()
            if msg is None:
                await b.put(None)
                break
            await b.put(msg)

    asyncio.create_task(listener_loop())
    asyncio.create_task(forward_logs())
    return b

async def main():
    a = await log_scribe()  # Call the scribe to start the play
    b = await log_listener(a)  # Listener joins without delay

    await a.put("First log message")  # Write some logs to channel A
    await a.put("Second log message")  # See them printed, clear as day

    await asyncio.sleep(1)  # A short pause to let them show

    await a.put(None)  # Close A, and end the flow
    await b.put(None)  # And B as well, for the curtain call

# Run the main function
asyncio.run(main())
# ==> 
# Logging: First log message
# Logging: Second log message

```
* 一次性返回的llm
```python
# https://github.com/BerriAI/litellm-staging
from litellm import acompletion
import asyncio
# print(asyncio.run(test_get_response(q))) => ModelResponse(id='chatcmpl-9cRAjj55YDmx94BNkLdos2Vyh7Rb5', choices=[Choices(finish_reason='stop', index=0, message=Message(content='Hello! How can I help you today?', role='assistant'))], created=1718947941, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint=None, usage=Usage(completion_tokens=9, prompt_tokens=8, total_tokens=17))
async def test_get_response(q):
    user_message = q #"Hello, how are you?"
    messages = [{"content": user_message, "role": "user"}]
    response = await acompletion(model="gpt-3.5-turbo", messages=messages)
    return response
print(asyncio.run(test_get_response("hi")))
```
## Python单文件执行快速验证概念

```elisp
;; jim-eval-buffer.el
(defun jw-eval-buffer ()
  "Evaluate the current buffer and display the result in a buffer."
  (interactive)
  (save-buffer)
  (let* ((file-name (buffer-file-name (current-buffer)))
         (file-extension (file-name-extension file-name))
         (buffer-eval-command-pair (assoc file-extension jw-eval-buffer-commands)))
    (if buffer-eval-command-pair
        (let ((command (concat (cdr buffer-eval-command-pair) " " file-name)))
          (shell-command-on-region (point-min) (point-max) command jw-eval-buffer-name nil)
          (pop-to-buffer jw-eval-buffer-name)
          (other-window 1)
          (jw-eval-buffer-pretty-up-errors jw-eval-buffer-name)
          (message ".."))
      (message "Unknown buffer type"))))
```

## Python remote repl for debug不要在线上编程

```elisp
;; TODO: kungfu_todo_for_ipython.el 改成IPython的版本 
(defun drb-shell (cmd fn &rest args)
  (let* ((args
	  (if (null args) ""
	    (concat " '" (reduce (lambda (s i) (concat s "' '" i)) args) "' ") ))
	 (cmd-str
	  (concat "drb" kungfu-path
		  "/drb-help/" cmd ".drb " args)))
    (funcall fn (shell-command-to-string cmd-str))))
```

## Emacs yasnippet帮助快速写脚手架代码, 算法脚手架

```elisp
(yas-define-snippets
 'python-mode
 '(("def" "def ${1:function_name}(${2:args}):\n    $0" "Python function")
   ("def" "def ${1:function_name}(${2:args}):\n    \"\"\"${3:Docstring for ${1}}\"\"\"\n    ${0:# TODO: ${1}}" "Python function with same variable in multiple places")
   ;; press tab will jump to next point for edit
   ("async" "async def ${1:function_name}(${2:args}):\n    ${0:# TODO: }\n\n${3:python-function}\n\nawait ${1}(${2})" "async await") ;; $0是最后回到的点。
   ))

(yas-define-snippets
 'ruby-mode
 '(("puts" "
puts -> {
  ${1:funs}
}[]
" "jimw eval buffer")))

```

## Python lambda演算
* Lisp 元编程 =》 Ruby 元编程 =》Python是Ruby的阉割版 。用Elisp来生成Python！用Clojure/Elisp/Ruby来学习转移帮助Python代码生成测试开发

```ruby
puts -> {
  # Ruby lambda快速演算 => TODO Python
  add = -> a { a + 1}
  add[100] #=> 101
}[]
```

## 快速万能同步转异步语法

```python
import asyncio
import sync2asyncio as s2a
s2a.simple_run_in_executor(time.sleep, 5) # 等效 await asyncio.sleep(5)
#=> <coroutine object simple_run_in_executor at 0x1320cc760>

# 运行coroutine对象或者运行异步函数: 不适用于 event loop： *** RuntimeError: asyncio.run() cannot be called from a running event loop
asyncio.run(s2a.simple_run_in_executor(time.sleep, 5))

```

