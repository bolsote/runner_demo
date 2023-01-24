import pytest
from hypothesis import given
from hypothesis.strategies import builds, integers

from runner_demo import (
    InvalidVersion,
    Version,
    VersionStore,
    format_version,
    parse_version,
)

SAMPLES = (
    ("1.0.0", (1, 0, 0)),
    ("1.2.0", (1, 2, 0)),
    ("1.2.3", (1, 2, 3)),
    ("1.0.4", (1, 0, 4)),
    ("0.0.1", (0, 0, 1)),
    ("0.1.0", (0, 1, 0)),
    ("0.1.2", (0, 1, 2)),
    ("1.2.3-alpha.1", (1, 2, 3, "alpha.1", None)),
    ("1.2.3+deadbeef", (1, 2, 3, None, "deadbeef")),
    ("1.2.3-alpha.1+deadbeef", (1, 2, 3, "alpha.1", "deadbeef")),
)


@pytest.mark.parametrize("version_string, version", SAMPLES)
def test_parser(version_string, version):
    assert parse_version(version_string) == Version(*version)


@pytest.mark.parametrize("version_string, version", SAMPLES)
def test_formatter(version_string, version):
    assert format_version(Version(*version)) == version_string


@pytest.mark.parametrize(
    "version_string",
    (
        "a.b.c",
        "1.2.z",
        "1.v.0",
    ),
)
def test_break_parser(version_string):
    with pytest.raises(InvalidVersion):
        parse_version(version_string)


@pytest.fixture
def store():
    return VersionStore()


def test_store(store):
    store.store("foo", "1.2.3")
    store.store("exp", "1.2.3-alpha.3")
    store.store("det", "1.2.3+deadbeef")

    assert store.load("foo") == Version(1, 2, 3)
    assert store.load("exp") == Version(1, 2, 3, "alpha.3")
    assert store.load("det") == Version(1, 2, 3, None, "deadbeef")


@given(
    builds(
        Version,
        major=integers(min_value=0),
        minor=integers(min_value=0),
        patch=integers(min_value=0),
    )
)
def test_inverse(version):
    assert version == parse_version(format_version(version))
