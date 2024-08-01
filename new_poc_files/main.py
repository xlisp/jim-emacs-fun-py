import pytest
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        logging.info('Starting pytest')
        pytest.main(['llm_test/c.py', 'llm_test/a.py', 'llm_test/b.py'])
    except Exception as e:
        logging.error(f'Error running pytest: {e}')