from transports import Transports


class TestTransport(Transports):
    """
    This is a fake transport used only during the UnitTests.
    Uses a string to store the sent message and can generate
    answers.
    """
    def __init__(self):
        Transports.__init__(self)
        self.wrote = None

    def _wrote(self):
        return self.wrote

    def open(self):
        pass

    def write(self, value):
        self.wrote = value

    def read(self):
        pass
