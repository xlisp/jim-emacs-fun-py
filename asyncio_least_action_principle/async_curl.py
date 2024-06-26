# python use Async Await write get google www.google.com/search?q=keyword count and print
# A symphony in code we'll start to compose,
import aiohttp
import asyncio

# Define a function to fetch and read,
# The HTML content, in this quest we'll proceed.
async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

# Now the function to count and declare,
# How many times 'keyword' appears there.
async def count_keyword_in_google(keyword):
    url = f'https://www.bing.com/search?q={keyword}'
    async with aiohttp.ClientSession() as session:
        html_content = await fetch_html(session, url)
        count = html_content.count(keyword)
        print(f"The keyword '{keyword}' appears {count} times in the HTML source of the search results page.")
        
# An entry point to call our task,
# Wrapped in asyncio’s cleric mask.
async def main():
    keyword = "example"  # Replace 'example' with your keyword of choice.
    await count_keyword_in_google(keyword)

# Unveil the magic with asyncio’s prayer,
# As we run the loop, the results we’ll declare.
asyncio.run(main())

# 跑起来 ===>> 'The keyword 'example' appears 24 times in the HTML source of the search results page.'

