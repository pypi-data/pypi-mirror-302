import os
import logging
import inspect

import yaml

__all__ = [
    "django_environ_settings_patch_all",
    "update_django_conf_settings",
]
DEFAULT_NAMESPACE = "DJANGO_"
_django_conf_settings_globals = None


class Null(object):
    pass


Null = Null()


def patch_items(namespace=DEFAULT_NAMESPACE):
    for key, value in os.environ.items():
        if key.startswith(namespace):
            real_key = key[len(namespace) :]
            value = yaml.safe_load(value)
            logging.warning(
                "Load setting from OS ENVIRONMENTS, env_key=%s, django_key=%s",
                key,
                real_key,
            )
            update_django_conf_settings(real_key, value)


def patch_keys(keys):
    keys = keys or []
    for key in keys:
        value = os.environ.get(key, Null)
        if value != Null:
            value = yaml.safe_load(value)
            logging.warning(
                "Load setting from OS ENVIRONMENTS, env_key=%s, django_key=%s",
                key,
                key,
            )
            update_django_conf_settings(key, value)


def patch_mapping_keys(mapping_keys):
    mapping_keys = mapping_keys or {}
    for env_key, django_key in mapping_keys.items():
        value = os.environ.get(env_key, Null)
        if value != Null:
            value = yaml.safe_load(value)
            logging.warning(
                "Load setting from OS ENVIRONMENTS, env_key=%s, django_key=%s",
                env_key,
                django_key,
            )
            update_django_conf_settings(django_key, value)


def django_environ_settings_patch_all(
    keys=None,
    mapping_keys=None,
    namespace=DEFAULT_NAMESPACE,
):
    patch_keys(keys=keys)
    patch_mapping_keys(mapping_keys=mapping_keys)
    patch_items(namespace=namespace)


def load_django_conf_settings_globals():
    global _django_conf_settings_globals
    frame = inspect.currentframe()
    while True:
        if not frame:
            break
        if frame.f_globals["__name__"] == os.environ.get("DJANGO_SETTINGS_MODULE"):
            break
        else:
            frame = frame.f_back
    if frame:
        _django_conf_settings_globals = frame.f_globals


def update_django_conf_settings(key, value):
    if _django_conf_settings_globals:
        _django_conf_settings_globals[key] = value


load_django_conf_settings_globals()
