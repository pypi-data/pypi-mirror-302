import pytest

import misa_openai
from misa_openai.lib._old_api import APIRemovedInV1


def test_basic_attribute_access_works() -> None:
    for attr in dir(misa_openai):
        dir(getattr(misa_openai, attr))


def test_helpful_error_is_raised() -> None:
    with pytest.raises(APIRemovedInV1):
        misa_openai.Completion.create()  # type: ignore

    with pytest.raises(APIRemovedInV1):
        misa_openai.ChatCompletion.create()  # type: ignore
