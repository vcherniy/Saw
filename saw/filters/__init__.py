import os
import glob
import inspect
from saw.mods import Mod

class Filter:
    _filters = dict()

    @classmethod
    def load_filters(cls):
        cls._filters = Mod.load_modules(__file__, 'saw.filters')

    @classmethod
    def exists(cls, name):
        return name in cls._filters

    @classmethod
    def get(cls, filter_name, item):
        if not(cls.exists(filter_name)):
            raise Exception("Filter not found!")
        # get class name of input variable and call filter's method with its name.
        func_name = item.__class__.__name__.lower()
        filter_class = cls._filters[filter_name]
        if not hasattr(filter_class, func_name):
            raise Exception("Filter '%s' has not method '%s'!" % (filter_name, func_name))

        def callback(*args, **kw):
            return getattr(filter_class(), func_name)(item, *args, **kw)
        return callback


if __name__ == '__main__':
    Filter.load_filters()