import contextlib
import time
from typing import Generator


@contextlib.contextmanager
def timing_ctx(name: str) -> Generator[None, None, None]:
    t0 = time.time()

    try:
        yield
    finally:
        t1 = time.time()
        print(f"{name} took {t1 - t0} seconds")
        print()


@timing_ctx("get_latest_created_screenshot")
def get_latest_created_screenshot(s: str):
    print("Running get_latest_created_screenshot")
    print(s)

    with timing_ctx("timing_something_else"):
        print("which can be use also as a context manager")


get_latest_created_screenshot("test")

get_latest_created_screenshot("test2")
