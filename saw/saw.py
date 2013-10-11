class Saw_Items(list):
    def __getattr__(self, name):
        name = str(name)

        for _type in self.__dict__:
            result = Saw_Items()
            for item in self.__dict__[_type]:
                result.extend( getattr(item, name, []) )

            if result:
                return result

from saw.parser import Base

class Saw():
    def load(self, text):
        return Parse(text)
