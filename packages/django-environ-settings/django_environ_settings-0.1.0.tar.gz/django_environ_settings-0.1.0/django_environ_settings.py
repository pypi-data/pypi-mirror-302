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
            value = yaml.safe_load(value)
            logging.warning(
                "Load setting from OS ENVIRONMENTS, environment_key=%s", key
            )
            update_django_conf_settings(key, value)


def patch_keys(keys):
    keys = keys or []
    for key in keys:
        value = os.environ.get(key, Null)
        if value != Null:
            value = yaml.safe_load(value)
            logging.warning(
                "Load setting from OS ENVIRONMENTS, environment_key=%s", key
            )
            update_django_conf_settings(key, value)


def django_environ_settings_patch_all(
    keys=None,
    namespace=DEFAULT_NAMESPACE,
):
    patch_keys(keys=keys)
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
