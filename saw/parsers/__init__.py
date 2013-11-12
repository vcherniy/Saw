from saw.items import Items
from saw.item import Item
from saw.parsers.paragraphs import Paragraphs


class Parser:
    _type = ''

    @classmethod
    def load(cls, saw, text):
        children, item = Items(), Item()

        for item_text in cls.parse(text):
            if isinstance(item_text, list):
                item.after(item_text)
            elif cls.child_class:
                cls.child_class.load(item, item_text)
                continue
            else:
                item.text(item_text)

            children.append(item)
            item = Item()
        # When ._text or ._after were assigned, it items were
        # added to children
        if item.children:
            children.append(item)
        if children:
            saw.__dict__[cls._type] = saw.children = children

    @staticmethod
    def load_all(text):
        saw = Item()
        Paragraphs.load(saw, text)
        return saw