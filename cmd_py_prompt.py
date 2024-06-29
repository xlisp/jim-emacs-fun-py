#!/opt/anaconda3/bin/python

## 在上面是示例中我们实现了查看或搜索历史输入的功能，其实我们还可以更加充分地利用 history.txt 中记载的历史输入，在用户输入时进行提示。实现此功能只需要在调用 prompt 函数时指定 auto_suggest 的参数即可：

from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
 
while True:
    user_input = prompt('>>>', history=FileHistory('history.txt'), 
                        auto_suggest=AutoSuggestFromHistory())
    if user_input.strip().lower() == 'exit':
        break
    print(user_input)

