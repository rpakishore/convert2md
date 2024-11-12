from functools import wraps
from time import perf_counter, sleep
from typing import Any, Callable


def retry_on_exception(retries: int = 3, delay: float = 1) -> Callable:
    """
    Attempt to call a function, if it fails, try again with a specified delay.

    :param retries: The max amount of retries you want for the function call
    :param delay: The delay (in seconds) between each function retry
    :return:
    """

    # Don't let the user use this decorator if they are high
    if retries < 1 or delay <= 0:
        raise ValueError(f"Invalid arguments, {retries=}, {delay=}")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for i in range(
                1, retries + 1
            ):  # 1 to retries + 1 since upper bound is exclusive

                try:
                    print(f"Running ({i}): {func.__name__}()")
                    return func(*args, **kwargs)
                except Exception as e:
                    # Break out of the loop if the max amount of retries is exceeded
                    if i == retries:
                        print(f"Error: {repr(e)}.")
                        print(f'"{func.__name__}()" failed after {retries} retries.')
                        break
                    else:
                        print(f"Error: {repr(e)} -> Retrying...")
                        sleep(delay)  # Add a delay before running the next iteration

        return wrapper

    return decorator


def time_it(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:

        # Note that timing your code once isn't the most reliable option
        # for timing your code. Look into the timeit module for more accurate
        # timing.
        start_time: float = perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = perf_counter()

        print(
            f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute'
        )
        return result

    return wrapper
