import time
from functools import wraps


def print_execution_time(method):

    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        execution_time = time.time() - start_time
        print(f"Method:{method.__name__} took {execution_time * 1000} ms")
        return result

    return wrapper
