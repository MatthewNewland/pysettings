try:
    from functools import reduce
except ImportError:
    pass


from operator import getitem


class SettingsError(Exception):
    pass


def _get_dict(dict_, path):
    return reduce(getitem, path, dict_)


def _set_dict(dict_, path, val):
    reduce(getitem, path[:-1], dict_)[path[-1]] = val


class Backend:
    """Abstract base class for settings backends.

    This class does implement the in-memory storage (as a dict)
    """
    def __init__(self, org_name, app_name, dict_type=dict):
        self.org_name = org_name
        self.app_name = app_name
        self.store = dict_type()

    def value(self, key, type):
        if not isinstance(key, (tuple, list)):
            key = key.split('/')
        val = _get_dict(self.store, key)
        return type(val)

    def set_value(self, key, value):
        if not isinstance(key, (tuple, list)):
            key = key.split('/')
        _set_dict(self.store, key, value)

    # read and write to be implemented by subclasses

    def read(self):
        pass

    def write(self):
        pass


DEFAULT_BACKEND = None  # TODO: Implement


class Settings:

    def __init__(self, org_name, app_name, backend_type=DEFAULT_BACKEND):
        self.backend = backend_type(org_name, app_name)

    def value(self, key, type=str):
        return self.backend.value(key, type)

    def set_value(self, key, value):
        self.backend.set_value(key, value)
