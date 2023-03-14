import time

from logger import logger

def retry(num_retries, wait_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num_retries):
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    if i == num_retries - 1:
                        raise e
                    else:
                        logger.error(repr(e))
                        time.sleep(wait_seconds)
                else:
                    return result
        return wrapper
    return decorator
