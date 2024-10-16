# -*- coding: utf-8 -*-
"""libsm module

Module interface with AWS Secrets Manager and, LRU cache for hit less to AWS endpoint if any
"""
import base64
import logging

from libumccr.aws import sm_client
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
def get_secret(secret_name):
    """
    If you are in long-running process and querying rotating value from secret manager such as JWT token, you may
    clear the cache before get secret call. e.g.

        libumccr.aws.libsm.get_secret.cache_clear()

    See https://github.com/umccr/gridss-purple-linx-nf/pull/25/files

    :param secret_name:
    :return:
    """
    resp = sm_client().get_secret_value(
        SecretId=secret_name
    )

    if 'SecretString' in resp:
        return resp['SecretString']
    else:
        return base64.b64decode(resp['SecretBinary'])
