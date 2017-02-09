### jim-emacs-fun-py
* `M-x py-utf-8`
```emacs-lisp
(defun py-utf-8 ()
  (interactive)
  (insert "#!/usr/bin/python\n#-*-coding:utf-8 -*-\n")
  )
```
* lambda
```py
add = lambda a,b : a + b
print add(2,3)
```
* map
```py
map(len,['aaa','faag','stevech']) #=> [3, 4, 7]
```
* each 
```py
abc = ['aaa','faag','stevech']
for i in range(len(abc)):
    print len(abc[i])
```
* reduce
```py
reduce(lambda a,b : a + b,[2,3,4]) #=> 9
```
* filter
```py
filter(lambda x: x>0, [2, -5, 9, -7, 2, 5, 4, -1, 0, -3, 8]) #=> [2, 9, 2, 5, 4, 8]
```
