import pytest
from django.conf import LazySettings
from django.core.cache import BaseCache, caches


@pytest.fixture(autouse=True)
def media_root(
    settings: LazySettings,
    tmpdir_factory: pytest.TempPathFactory,
) -> None:
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True)
def password_hashers(settings: LazySettings) -> None:
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture(autouse=True)
def auth_backends(settings: LazySettings) -> None:

    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


@pytest.fixture(autouse=True)
def debug(settings: LazySettings) -> None:

    settings.DEBUG = False
    for template in settings.TEMPLATES:
        template['OPTIONS']['debug'] = True


@pytest.fixture(autouse=True)
def cache(settings: LazySettings) -> BaseCache:

    test_cache = 'test'

    settings.CACHES[test_cache] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
    settings.RATELIMIT_USE_CACHE = test_cache
    settings.AXES_CACHE = test_cache

    caches[test_cache].clear()
    return caches[test_cache]
