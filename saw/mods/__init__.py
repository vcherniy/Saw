import os
import glob
import inspect


class Mod:
    _mods = {
        'paragraphs': [],
        'sentences': [],
        'blocks': [],
        'words': []
    }
    loaded = False

    @staticmethod
    def load_modules(path, package_name):
        module_names = [os.path.basename(fname)[:-3].lower() for fname in glob.glob(os.path.dirname(path) + "/*.py")
                        if fname != '__init__.py']
        imported_modules = __import__(package_name, globals(), locals(), module_names, -1)

        result = dict()
        for module_name in module_names:
            module_obj = getattr(imported_modules, module_name)

            # import class from module what class name = module name
            for cls_name, cls in inspect.getmembers(module_obj):
                if (cls_name.lower() == module_name) and inspect.isclass(cls):
                    result[module_name] = cls
                    break
        return result

    @classmethod
    def init(cls):
        if cls.loaded:
            return
        result = cls.load_modules(__file__, 'saw.mods')

        for mod_name in result:
            for attr_name, attr in inspect.getmembers(result[mod_name]):
                if attr_name.lower() in cls._mods:
                    cls._mods[ attr_name.lower() ].append(attr)
        cls.loaded = True

    @classmethod
    def get(cls, name, data):
        if not(name in cls._mods):
            raise Exception("Mods not found!")

        for mod in cls._mods[name]:
            data = mod(*data)
        return data