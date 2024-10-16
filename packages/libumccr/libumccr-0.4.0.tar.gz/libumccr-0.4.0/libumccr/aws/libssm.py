# -*- coding: utf-8 -*-
"""libssm module

Mainly interface with SSM Parameter Store and, LRU cache for hit less to AWS endpoint if any
"""
import logging

from libumccr.aws import ssm_client
from libumccr.utils import load_package_if_found

logger = logging.getLogger(__name__)

if load_package_if_found("cachetools"):
    logger.debug(f"cachetools found, using LRU cache")
    from cachetools.func import lru_cache
else:
    def lru_cache(maxsize):
        logger.debug(f"cachetools not found, skipping LRU cache with maxsize={maxsize}")

        def wrapper(func):
            func.cache_clear = lambda: None
            return func

        return wrapper


@lru_cache(maxsize=64)
def get_secret(key) -> str:
    """
    Retrieve the secret value from SSM

    You can clear the cache before get secret call. e.g.

        libumccr.aws.libssm.get_secret.cache_clear()

    :param key: key of secret
    :return: the secret value
    """
    resp = ssm_client().get_parameter(
        Name=key,
        WithDecryption=True
    )
    return resp['Parameter']['Value']


def get_ssm_param(name):
    """
    Fetch the parameter with the given name from SSM Parameter Store.
    """
    return get_secret(name)


class SSMParamStore(object):
    def __init__(self, key):
        self._key = key
        self._value = None

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        assert self._key is not None, "Undefined key"
        return get_secret(self._key)

    def get_value(self):
        return self.value

    get: get_value

    def __str__(self):
        return f"{self._key}"
