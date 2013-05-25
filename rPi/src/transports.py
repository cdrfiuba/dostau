class Transports:
    """
    This is an abstract class which defines the interface that
    a transport object should have.
    """

    def __init__(self):
        pass

    def _to_string(self, cmd):
        """
        Transforms a list of integers into a string.

        :param cmd: command to send.
        :type cmd: int list
        :returns: the string representing the command.
        :rtype: string
        """
        return reduce(lambda s, c: s + chr(c), cmd, "")

    def _to_int_list(self, cmd_string):
        """
        Transforms a received string to a list of integers.

        :param cmd_string: the string-encoded command.
        :type cmd_string: string
        :returns: A integer list holding the commando.
        :rtype: int list
        """
        return [ord(c) for c in cmd_string]

    def open(self):
        """ Open the communication channel. """
        raise NotImplementedError("Not implemented.")

    def write(self, value):
        """
        Write a value to the channel.

        :param value: The data to send.
        :type value: int
        """
        raise NotImplementedError("Not implemented.")

    def read(self):
        """
        Write a value to the channel.

        :return: The data read.
        :rtype: int
        """
        raise NotImplementedError("Not implemented.")
