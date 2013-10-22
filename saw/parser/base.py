from ..saw import Items, Item

class Base:
    @classmethod
    def load(self, saw, text, ident):
        ident2 = ident + '.  '
        if not('children' in saw.__dict__):
            saw.__dict__['children'] = Items()
        saw.live()
        items = self.parse(text)

        item = Item(self)
        for item_text in items:
            if isinstance(item_text, list):
                print ident2 + self._type + ': ' + str(item_text) + ''
                item.after(item_text)
                
                saw.children.append(item)
                item = Item(self)
            elif self.child_class:
                print ident2 + self._type + ': ' + self.child_class.__name__ + '.load( ' + item_text + ') '
                item = self.child_class.load(item, item_text, ident2)
            else:
                print ident2 + self._type + ': << ' + item_text
                item.text(item_text)
                saw.children.append(item)
                item = Item(self)

        if item._live:
            saw.children.append(item)

        for a in saw.children:
            print ident2 + '_has: ' + self._type


        print ident2 + ' _____' + str(saw.children)
        if not (self._type in saw.__dict__):
            saw.__dict__[ self._type ] = saw.children
        #print saw.children
        return saw


from paragraphs import Paragraphs

class Parse:
    @staticmethod
    def load(text):
        saw = Item(Paragraphs)
        return Paragraphs.load(saw, text, '')