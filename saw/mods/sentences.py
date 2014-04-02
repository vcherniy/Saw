class Sentences:
    @staticmethod
    def sentences(before, string, after):
        while before and (before[-1].symbol == '.') and before[-1].none():
            string = before.pop().symbol + string
        if before and (before[-1].symbol == '.') and before[-1].left():
            string = before.pop().symbol + string
        return [before, string, after]

    @staticmethod
    def blocks(before, string, after):
        _ln = len(before)
        if _ln and (before[-1].symbol in ['-', '+', ':'])\
            and (before[-1].left() or (_ln == 1 and before[-1].none())):
            string = before.pop().symbol + string
        return [before, string, after]