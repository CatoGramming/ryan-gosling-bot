import pytest
from mimesis import Field, Locale


@pytest.fixture()
def fake() -> Field:
    return Field(locale=Locale.RU)
