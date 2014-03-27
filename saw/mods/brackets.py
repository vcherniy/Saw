class Brackets:
    @staticmethod
    def blocks(before, string, after):
        #{0}text{1} {0}  new {1} {0}{0}two{1}{1} {0} {0} aaa {1} {1}

        for i in xrange(0, len(after)):
            if after[i].strip() in [']', ')']:
                after[i] = after[i].strip()
            elif len(after[i]) > 1:
                break

        for i in xrange(len(before) - 1, -1, -1):
            if before[i].strip() in ['[', '(']:
                before[i] = before[i].strip()
            elif len(before[i]) > 1:
                break

        return [before, string, after]
        """
        _ln = len(after)
        i = 0
        while i < _ln:
        if after[i].stip() == ')':


        while before and before[-1] in ['']
        return [before, string, after]"""