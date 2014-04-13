from saw.mods import Mod


class Filter:
    _filters = dict()
    _loaded = False

    @classmethod
    def init(cls):
        if cls._loaded:
            return
        cls._filters = Mod.load_modules(__file__, 'saw.filters')
        cls._loaded = True

    @classmethod
    def exists(cls, name):
        cls.init()
        return name in cls._filters

    @classmethod
    def get(cls, filter_name, item):
        if not cls.exists(filter_name):
            raise Exception("Filter not found!")
        # get class name of input variable and call filter's method with its name.
        func_name = item.__class__.__name__.lower()
        filter_class = cls._filters[filter_name]
        if not hasattr(filter_class, func_name):
            raise Exception("Filter '%s' has not method '%s'!" % (filter_name, func_name))

        def callback(*args, **kw):
            return getattr(filter_class(), func_name)(item, *args, **kw)
        return callback