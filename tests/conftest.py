import pkgutil
import sys
from typing import List

import os
from _pytest.config import Parser
from _pytest.python import Metafunc

base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)


def explore_pytest_plugins(base_dir: str,
                           fixtures_pkg_name: str) -> List[str]:
    fixtures_pkg_path = os.path.join(base_dir,
                                     fixtures_pkg_name)
    return [fixtures_pkg_name + '.' + name
            for _, name, _ in pkgutil.iter_modules([fixtures_pkg_path])]


pytest_plugins = explore_pytest_plugins(base_dir=base_dir,
                                        fixtures_pkg_name='fixtures')


def pytest_addoption(parser: Parser) -> None:
    parser.addoption('--repeat',
                     action='store',
                     help='Number of times to repeat each test.')


def pytest_generate_tests(metafunc: Metafunc) -> None:
    if metafunc.config.option.repeat is None:
        return
    count = int(metafunc.config.option.repeat)
    # We're going to duplicate these tests by parametrisation,
    # which requires that each test has a fixture to accept the parameter.
    # We can add a new fixture like so:
    metafunc.fixturenames.append('tmp_ct')
    # Now we parametrize. This is what happens when we do e.g.,
    # @pytest.mark.parametrize('tmp_ct', range(count))
    # def test_foo(): pass
    metafunc.parametrize('tmp_ct', range(count))
