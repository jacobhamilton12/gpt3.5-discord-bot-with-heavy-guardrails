import time
import signal
from functools import wraps

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

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message='Function call timed out'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutError(error_message)

            old_handler = signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

            return result

        return wrapper

    return decorator
