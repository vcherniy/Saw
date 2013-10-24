from ..saw import Items, Item

class Base:
    @classmethod
    def load(self, saw, text):
        children, item = Items(), Item()

        for item_text in self.parse(text):
            if isinstance(item_text, list):
                item.after(item_text)
            elif self.child_class:
                self.child_class.load(item, item_text)
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
            saw.__dict__[ self._type ] = saw.children = children

from paragraphs import Paragraphs

class Parse:
    @staticmethod
    def load(text):
        saw = Item()
        Paragraphs.load(saw, text)
        return saw