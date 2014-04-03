class Brackets:
    @staticmethod
    def blocks(before, string, after):
        # just one ( or [ in before
        # just one ] or ) in after
        # ( or [ on begin of before
        # ] or ) on end of after
        # no ( or [ on after
        # no ) or ] on before

        for i in xrange(0, len(after)):
            if after[i].strip() in [']', ')']:
                after[i] = after[i].strip() + ' '
                
        #for i in xrange(len(before) - 1, -1, -1):
        #    if before[i].strip() in ['[', '(']:
        #        before[i] = before[i].strip()
        #    elif len(before[i]) > 1:
        #        break

        return [before, string, after]
        """
        _ln = len(after)
        i = 0
        while i < _ln:
        if after[i].stip() == ')':


        while before and before[-1] in ['']
        return [before, string, after]"""