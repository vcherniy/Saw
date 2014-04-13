class Asterisk:
    @staticmethod
    def blocks(before, string, after):
        if before:
            join = True
            for item in before:
                if item != '*':
                    join = False
                    break
            if join:
                string = ''.join(before) + string
                before = []
        return [before, string, after]
