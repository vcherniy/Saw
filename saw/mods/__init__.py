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

    @classmethod
    def load_mods(cls):
        if cls._mods_class:
            return

        curr_path = os.path.dirname(__file__)
        module_names = [os.path.basename(fname)[:-3].lower() for fname in glob.glob(curr_path + "/*.py")
                        if fname != '__init__.py']
        mods = __import__('saw.mods', globals(), locals(), module_names, -1)

        for module_name in module_names:
            mod_module = getattr(mods, module_name)

            for obj_name, obj in inspect.getmembers(mod_module):
                if (obj_name.lower() == module_name) and inspect.isclass(obj):
                    cls._mods_class[obj_name] = obj

                    for attr_name, attr in inspect.getmembers(obj):
                        if attr_name.lower() in cls._mods:
                            cls._mods[ attr_name.lower() ].append(obj_name)

    @classmethod
    def get(cls, name: str, data: list):
        if not(name in cls._mods):
            raise Exception("Mods not found!")

        for class_name in cls._mods[name]:
            func = getattr(cls._mods_class[class_name](), name, None)
            if func:
                data = func(*data)
        return data