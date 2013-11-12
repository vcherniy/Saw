import os
import glob
import inspect


class Filter:
    _filters = dict()

    @classmethod
    def load_filters(cls):
        curr_path = os.path.dirname(__file__)
        module_names = [os.path.basename(fname)[:-3].lower() for fname in glob.glob(curr_path + "/*.py")
                        if fname != '__init__.py']
        filters = __import__('saw.filters', globals(), locals(), module_names, -1)

        for module_name in module_names:
            filter_module = getattr(filters, module_name)

            for obj_name, obj in inspect.getmembers(filter_module):
                if (obj_name.lower() == module_name) and inspect.isclass(obj):
                    cls._filters[module_name] = obj
                    break

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