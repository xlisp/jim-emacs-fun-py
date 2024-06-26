#!/opt/anaconda3/bin/python

import asyncio
from pyppeteer import launch

## 上面代码中，启动浏览器（launch）、打开新 Tab（newPage()）、访问网址（page.goto()）、截图（page.screenshot()）、关闭浏览器（browser.close()），这一系列操作都是异步任务，使用 await 命令写起来非常自然简单。

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.run(main())

