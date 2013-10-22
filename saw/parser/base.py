from ..saw import Items, Item

class Base:
    @classmethod
    def load(self, saw, text):
        children = Items()
        saw.live()

        items = self.parse(text)

        item = Item()
        for item_text in items:
            if isinstance(item_text, list):
                item.after(item_text)
                
                children.append(item)
                item = Item()
            elif self.child_class:
                self.child_class.load(item, item_text)
            else:
                item.text(item_text)
                children.append(item)
                item = Item()

        if item._live:
            children.append(item)

        if children:
            saw.__dict__[ self._type ] = saw.children = children

from paragraphs import Paragraphs

class Parse:
    @staticmethod
    def load(text):
        saw = Item()
        Paragraphs.load(saw, text)
        return saw