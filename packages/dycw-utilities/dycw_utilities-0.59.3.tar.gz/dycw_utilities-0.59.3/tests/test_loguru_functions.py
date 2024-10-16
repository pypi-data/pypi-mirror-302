from __future__ import annotations

from time import sleep

from loguru import logger
from tenacity import retry, wait_fixed

from utilities.loguru import LogLevel, log
from utilities.tenacity import before_sleep_log

# eventkit


def func_test_eventkit(n: int, /) -> None:
    logger.trace("n={n}", n=n)


# loguru


def func_test_log_disable(x: int, /) -> int:
    with log(disable=True):
        return x + 1


def func_test_log_entry(x: int, /) -> int:
    with log():
        return x + 1


def func_test_log_entry_disabled(x: int, /) -> int:
    with log(entry_level=None):
        return x + 1


def func_test_log_entry_non_default_level(x: int, /) -> int:
    with log(entry_level=LogLevel.DEBUG):
        return x + 1


def func_test_log_error(x: int, /) -> int | None:
    with log():
        if x % 2 == 0:
            return x + 1
        msg = f"Got an odd number: {x}"
        raise ValueError(msg)


def func_test_log_error_expected(x: int, /) -> int | None:
    with log(error_expected=ValueError):
        if x % 2 == 0:
            return x + 1
        msg = f"Got an odd number: {x}"
        raise ValueError(msg)


def func_test_log_exit_explicit(x: int, /) -> int:
    with log(exit_level=LogLevel.DEBUG):
        return x + 1


def func_test_log_exit_duration(x: int, /) -> int:
    with log(exit_duration=0.0):
        sleep(0.01)
        return x + 1


def func_test_log_contextualize(x: int, /) -> int:
    with log(key="value"):
        return x + 1


def func_test_log_exit_variable(x: int, /) -> int:
    with log(exit_level=LogLevel.DEBUG) as log_cap:
        return log_cap(x + 1)


def func_test_log_exit_variable_disable(x: int, /) -> int:
    with log(disable=True, exit_level=LogLevel.DEBUG) as log_cap:
        return log_cap(x + 1)


# tenacity


_counter = 0


@retry(wait=wait_fixed(0.01), before_sleep=before_sleep_log())
def func_test_tenacity_before_sleep_log() -> int:
    global _counter  # noqa: PLW0603
    _counter += 1
    if _counter >= 3:
        return _counter
    raise ValueError(_counter)
