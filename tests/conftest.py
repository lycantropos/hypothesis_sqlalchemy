import os
import platform
import time
from collections.abc import Callable, Iterator
from datetime import timedelta
from typing import cast

import pytest
from hypothesis import HealthCheck, settings

is_pypy = platform.python_implementation() == 'PyPy'
on_ci = bool(os.getenv('CI'))
max_examples = (
    -(-settings().max_examples // 10)
    if is_pypy and on_ci
    else settings().max_examples
)
settings.register_profile(
    'default',
    deadline=(timedelta(hours=1) / max_examples if on_ci else None),
    max_examples=max_examples,
    suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow],
)

# FIXME:
#  workaround until https://github.com/pytest-dev/pluggy/issues/191 is fixed
hookimpl = cast(
    Callable[..., Callable[[Callable[..., None]], Callable[..., None]]],
    pytest.hookimpl,
)

if on_ci:
    time_left = timedelta(hours=1)

    @hookimpl(tryfirst=True)
    def pytest_runtest_call(item: pytest.Function) -> None:
        set_deadline = settings(deadline=time_left / max_examples)
        item.obj = set_deadline(item.obj)

    @pytest.fixture(autouse=True)
    def time_function_call() -> Iterator[None]:
        start = time.monotonic()
        try:
            yield
        finally:
            duration = timedelta(seconds=time.monotonic() - start)
            global time_left
            time_left = max(duration, time_left) - duration


@hookimpl(trylast=True)
def pytest_sessionfinish(
    session: pytest.Session, exitstatus: pytest.ExitCode
) -> None:
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        session.exitstatus = pytest.ExitCode.OK
