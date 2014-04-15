class Sentences:
    @staticmethod
    def sentences(before, string, after, first):
        while before and (before[-1] == '.'):
            string = before.pop().strip() + string
        if before and (before[-1] == ' .'):
            string = before.pop().strip() + string
        return [before, string, after]

    @staticmethod
    def blocks(before, string, after, first):
        _ln = len(before)
        if (_ln == 1 and before[0] in ['-', '+', ':', ' -', ' +', ' :'])\
                or (_ln > 1 and before[-1] in [' -', ' +', ' :']):
            string = before.pop().strip() + string
        return [before, string, after]