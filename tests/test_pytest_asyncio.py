import asyncio
import pytest
pytest_plugins = ('pytest_asyncio',)
@pytest.mark.asyncio
async def test_simple():
    await asyncio.sleep(0.5)
