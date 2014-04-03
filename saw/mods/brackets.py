class Brackets:
    @classmethod
    def blocks(cls, before, string, after):
        # just one ( or [ in before
        # just one ] or ) in after
        # ( or [ on begin of before
        # ] or ) on end of after
        # no ( or [ on after
        # no ) or ] on before
        cls._process(before)
        cls._process(after)
        
        return [before, string, after]

    @staticmethod
    def _process(items):
        if items:
            for i in xrange(0, len(items)):
                item = items[i].strip()
                if item in [']', ')']:
                    items[i] = item + ' '
                if item in ['(', '[']:
                    items[i] = '  ' + item

            # if x- ) then include ) to -
            before_bracket = items[0] in [') ', '] ']
            for i in xrange(1, len(items)):
                if items[i] in [') ', '] ']:
                    if not before_bracket and (items[i - 1][-1] == ' '):
                        items[i - 1] = items[i - 1][:-1]
                    before_bracket = True
                else:
                    before_bracket = False

            # if '( - ' then include ( to -
            before_bracket = items[0] in ['  (', '  [']
            for i in xrange(1, len(items)):
                if not(items[i] in ['  (', '  [']):
                    if before_bracket and (items[i][0] == ' '):
                        items[i] = items[i][1:]
                    before_bracket = False
                else:
                    before_bracket = True