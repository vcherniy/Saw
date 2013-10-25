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
        module_names = [name for name in __all__ if not(name == '__init__') ]
        filters = __import__('saw.filters', globals(), locals(), module_names, -1)

        for name in module_names:
            module = getattr(filters, name)

            for obj_name, obj in inspect.getmembers(module):
                if (obj_name.lower() == name) and inspect.isclass(obj):
                    self._filters[ name ] = obj
                    break

    @classmethod
    def exists(self, name):
        return name in self._filters

    @classmethod
    def apply(self, name, item):
        if not(self.exists(name)):
            return False

        filter_class = self._filters[ name ]()
        if isinstance(item, saw.items.Items):
            return filter_class.items(item)
        else:
            return filter_class.item(item)

Filter._load_filters()