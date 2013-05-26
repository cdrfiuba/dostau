from transports import Transports


class TestTransport(Transports):
    """
    This is a fake transport used only during the UnitTests.
    Uses a string to store the sent message and can generate
    answers.
    """
    def __init__(self):
        Transports.__init__(self)
        self.wrote = []
        self.ans_buff = []

    def _wrote(self):
        return [self._to_int_list(c) for c in self.wrote]
        
    def _clean(self):
        self.wrote = []
        
    def _set_ans(self, ans):
        self.ans_buff = ans

    def open(self):
        pass

    def write(self, value):
        cmd = self._to_string(value)
        self.wrote.append(cmd)

    def read(self, size=1):
        return ans[:size]
