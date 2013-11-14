import os
import glob
import inspect


class Mod:
    _mods_class = {}
    _mods = {
        'paragraphs': [],
        'sentences': [],
        'blocks': [],
        'words': []
    }

    @staticmethod
    def load_modules(path, package_name):
        module_names = [os.path.basename(fname)[:-3].lower() for fname in glob.glob(os.path.dirname(path) + "/*.py")
                        if fname != '__init__.py']
        imported_modules = __import__(package_name, globals(), locals(), module_names, -1)

        result = dict()
        for module_name in module_names:
            module_obj = getattr(imported_modules, module_name)

            for obj_name, obj in inspect.getmembers(module_obj):
                if (obj_name.lower() == module_name) and inspect.isclass(obj):
                    result[module_name] = obj
                    break
        return result

    @classmethod
    def load_mods(cls):
        if cls._mods_class:
            return
        cls._mods_class = cls.load_modules(__file__, 'saw.mods')

        for mod_name in cls._mods_class:
            for attr_name, attr in inspect.getmembers(cls._mods_class[mod_name]):
                if attr_name.lower() in cls._mods:
                    cls._mods[ attr_name.lower() ].append(mod_name)

    @classmethod
    def get(cls, name: str, data: list):
        if not(name in cls._mods):
            raise Exception("Mods not found!")

        for class_name in cls._mods[name]:
            data = getattr(cls._mods_class[class_name](), name)(*data)
        return data