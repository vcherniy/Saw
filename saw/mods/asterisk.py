class Asterisk:
    @staticmethod
    def blocks(before, string, after):
        if before:
            join = True
            for item in before:
                if not(item.symbol == '*' and item.none()):
                    join = False
                    break
            if join:
                string = ''.join((x.symbol for x in before)) + string
                before = []
        return [before, string, after]