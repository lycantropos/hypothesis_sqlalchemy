import re

from hypothesis_sqlalchemy import __version__


def test_version() -> None:
    assert isinstance(__version__, str)
    assert is_semver(__version__)


SEMVER_PATTERN = re.compile(r'^(?P<major>[0-9]|[1-9][0-9]*)\.'
                            r'(?P<minor>[0-9]|[1-9][0-9]*)\.'
                            r'(?P<patch>[0-9]|[1-9][0-9]*)'
                            r'(?P<build>-([0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?$')


def is_semver(version_string: str) -> bool:
    return SEMVER_PATTERN.fullmatch(version_string) is not None
