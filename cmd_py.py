#!/opt/anaconda3/bin/python

# while True input(xxx) 就是最经典的命令行等待任务轮训！ => 回到命令行第一性原理上去！

while True:
    user_input = input('>')
    print(user_input)
    if user_input.strip().lower() == 'exit':
        break
