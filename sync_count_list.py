import time

def count():
    print("One")
    time.sleep(1)
    print("Two")

def main():
    for _ in range(3):
        count()

main()
# => 三个 count() 都是同步执行，必须等到前一个执行完，才能执行后一个。脚本总的运行时间是3秒。 => async_count_list.py 就只要一秒就完成了。
# One
# Two
# One
# Two
# One
# Two
#
