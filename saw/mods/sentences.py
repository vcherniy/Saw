class Sentences:
    @staticmethod
    def sentences(before, string, after):
        while before and (before[-1] == '.'):
            string = before.pop().strip() + string
        if before and (before[-1] == ' .'):
            string = before.pop().strip() + string
        return [before, string, after]

    @staticmethod
    def blocks(before, string, after):
        while before and (before[-1] == '-'):
            string = before.pop().strip() + string
        if before and (before[-1] == ' -'):
            string = before.pop().strip() + string
        return [before, string, after]