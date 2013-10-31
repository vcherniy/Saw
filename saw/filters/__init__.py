import os
import glob
import inspect
import saw.items

curr_path = os.path.dirname(__file__)
__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(curr_path + "/*.py")]

class Filter:
    _filters = dict()

    @classmethod
    def _load_filters(self):
        module_names = [ name.lower() for name in __all__ if name != '__init__' ]
        filters = __import__('saw.filters', globals(), locals(), module_names, -1)

        for module_name in module_names:
            _filter = getattr(filters, module_name)

            for obj_name, obj in inspect.getmembers(_filter):
                if (obj_name.lower() == module_name) and inspect.isclass(obj):
                    self._filters[ module_name ] = obj
                    break

    @classmethod
    def exists(self, name):
        return name in self._filters

    @classmethod
    def get(self, name, item):
        if not(self.exists(name)):
            raise Exception("Filter not found!")

        filter_class = self._filters[ name ]()
        if isinstance(item, saw.items.Items):
            func = filter_class.items
        else:
            func = filter_class.item

        def _call(*args, **kw):
            return func(item, *args, **kw)
        return _call


Filter._load_filters()