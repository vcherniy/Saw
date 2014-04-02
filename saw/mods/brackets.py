class Brackets:
    @classmethod
    def sblocks(cls, before, string, after):
        # just one ( or [ in before
        # just one ] or ) in after
        # ( or [ on begin of before
        # ] or ) on end of after
        # no ( or [ on after
        # no ) or ] on before
        before = cls._process(before)
        after = cls._process(after)
        print [before, string, after]

        return [before, string, after]
        """
        _ln = len(after)
        i = 0
        while i < _ln:
        if after[i].stip() == ')':


        while before and before[-1] in ['']
        return [before, string, after]"""

    @staticmethod
    def _process(items):
        _len = len(items)

        for i in xrange(0, _len):
            if items[i].strip() in [']', ')']:
                items[i] = items[i].strip() + ' '
                
        for i in xrange(-1, -1 * _len, -1):
            items[i]
        return items