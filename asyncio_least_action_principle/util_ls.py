
## 1111 asyncio监视器，app-state方法
asyncio.current_task # 返回当前运行的 Task 实例，如果没有正在运行的任务则返回 None。
# 如果 loop 为 None 则会使用 get_running_loop() 获取当前事件循环。


asyncio.all_tasks # 返回事件循环所运行的未完成的 Task 对象的集合。

asyncio.iscoroutine # 如果 obj 是一个协程对象则返回 True。
