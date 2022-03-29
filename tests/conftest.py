import os
from datetime import timedelta

import pytest
from hypothesis import (HealthCheck,
                        settings)

on_ci = bool(os.getenv('CI', False))
max_examples = settings.default.max_examples
settings.register_profile('default',
                          deadline=(timedelta(hours=1) / max_examples
                                    if on_ci
                                    else None),
                          max_examples=max_examples,
                          suppress_health_check=[HealthCheck.too_slow,
                                                 HealthCheck.filter_too_much])


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session,
                         exitstatus: pytest.ExitCode) -> None:
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        session.exitstatus = pytest.ExitCode.OK
