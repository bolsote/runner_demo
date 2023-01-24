import typing

import attrs


@attrs.frozen
class Version:
    major: int = attrs.field(validator=attrs.validators.ge(0))
    minor: int = attrs.field(validator=attrs.validators.ge(0))
    patch: int = attrs.field(validator=attrs.validators.ge(0))
    extra: typing.Optional[str] = None
    build: typing.Optional[str] = None


class InvalidVersion(Exception):
    ...


def parse_version(version_string: str) -> Version:
    if not version_string:
        raise InvalidVersion

    core = version_string
    extra = None
    build = None

    if "+" in core:
        core, build = core.split("+")
    if "-" in core:
        core, extra = core.split("-")

    major_str, minor_str, patch_str = core.split(".")

    try:
        major = int(major_str)
        minor = int(minor_str)
        patch = int(patch_str)
    except ValueError as exc:
        raise InvalidVersion from exc

    return Version(major, minor, patch, extra, build)


def format_version(version: Version) -> str:
    version_string = f"{version.major}.{version.minor}.{version.patch}"

    if version.extra:
        version_string += f"-{version.extra}"
    if version.build:
        version_string += f"+{version.build}"

    return version_string


class VersionStore:
    def __init__(self, validator: typing.Callable[[str], Version] = parse_version):
        self._store: dict[str, Version] = {}
        self._validator = validator

    def load(self, package: str) -> typing.Optional[Version]:
        return self._store.get(package, None)

    def store(self, package: str, version_string: str) -> None:
        version = self._validator(version_string)
        self._store[package] = version
