import re

import hypothesis_sqlalchemy


def test_version() -> None:
    version_string = hypothesis_sqlalchemy.__version__

    assert isinstance(version_string, str)
    assert is_semver(version_string)


SEMVER_PATTERN = re.compile(r'^(?P<major>[0-9]|[1-9][0-9]*)\.'
                            r'(?P<minor>[0-9]|[1-9][0-9]*)\.'
                            r'(?P<patch>[0-9]|[1-9][0-9]*)'
                            r'(?P<build>:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))'
                            r'?$')


def is_semver(version_string: str) -> bool:
    return SEMVER_PATTERN.fullmatch(version_string) is not None
