class Pure:
    def item(self, item):
        new_item = item.__class__()
        new_item.__dict__ = item.__dict__.copy()
        new_item.after([])
        return new_item

    def items(self, items):
        return items.__class__( x.pure() for x in items )