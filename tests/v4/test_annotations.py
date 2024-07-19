from aio_taginfo.api.v4._internal import NonEmptyString, OptionalHttpUrl, OptionalNonEmptyString

import pytest
from pydantic import ValidationError
from pydantic.dataclasses import dataclass


def test_non_empty_string():
    @dataclass(kw_only=True, frozen=True)
    class MyClass:
        key: NonEmptyString

    with pytest.raises(ValidationError):
        MyClass(key=None)

    with pytest.raises(ValidationError):
        MyClass(key="")

    with pytest.raises(ValidationError):
        MyClass(key="   ")

    assert MyClass(key="some key").key == "some key"
    assert MyClass(key="   some key ").key == "some key"


def test_optional_non_empty_string():
    @dataclass(kw_only=True, frozen=True)
    class MyClass:
        key: OptionalNonEmptyString

    assert MyClass(key=None).key is None
    assert MyClass(key="").key is None
    assert MyClass(key="   ").key is None
    assert MyClass(key="some key").key == "some key"
    assert MyClass(key="   some key ").key == "some key"

    with pytest.raises(ValidationError):
        MyClass(key=42)


def test_optional_http_url():
    @dataclass(kw_only=True, frozen=True)
    class MyClass:
        url: OptionalHttpUrl

    assert MyClass(url="").url is None
    assert MyClass(url="     ").url is None
    assert MyClass(url="https://taginfo.openstreetmap.org").url is not None
    assert MyClass(url="   https://taginfo.openstreetmap.org ").url is not None
