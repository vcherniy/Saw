class Pure:
    @staticmethod
    def item(item):
        new_item = item.__class__()
        new_item.__dict__ = item.__dict__.copy()
        new_item.after([])
        return new_item

    @staticmethod
    def items(items):
        return items.__class__(x.pure() for x in items)