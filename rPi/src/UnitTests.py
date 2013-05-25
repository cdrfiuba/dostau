import unittest
import math
from protocol import CMDS
from test_transport import TestTransport
from m3pi import M3pi


class TestTestTransport(unittest.TestCase):
    """
    Tests that the mock transport correctly records the sent data
    and answers with the correct values.
    """

    def setUp(self):
        self.tr = TestTransport()

    def test_to_string(self):
        """
        The transport class should transform the commands from list of numbers
        to strings.
        """
        cmd = [0x54, 0x45, 0x53, 0x54]
        cmd_string = self.tr._to_string(cmd)
        self.assertEqual(cmd_string, 'TEST')

    def test_to_lit(self):
        """
        The transport class should be able to transform from the received
        string to a list of ints.
        """
        cmd_list = self.tr._to_int_list('TEST')
        gt = (0x54, 0x45, 0x53, 0x54)
        self.assertEqual(tuple(cmd_list), gt)

    def test_write(self):
        """
        Tests that I can read a value that was written to the transport.
        """
        test_cmd = CMDS['M1_FORWARD']
        self.tr.write(test_cmd)
        cmd = self.tr._wrote()
        self.assertEqual(test_cmd, cmd)


class Testm3pi(unittest.TestCase):
    """
    Tests the communication protocol with the 3pi robot.
    """

    def setUp(self):
        self.tr = TestTransport()
        self.robot = M3pi(self.tr)

    def test_set_motor_speed(self):
        """
        Tests that the set motor speed function sends the correct values.
        It should send the command stating the motor and direction and then the
        speed value in absolute value multiplied by 0x7f
        """
        self.robot._set_motor_speed(1, 1)
        gt = (CMDS['M1_FORWARD'], 0x7f * abs(1))
        wrote = self.tr._wrote()
        self.assertEqual(tuple(wrote), gt)

        self.robot._set_motor_speed(2, 1)
        gt = (CMDS['M2_FORWARD'], 0x7f * abs(1))
        wrote = self.tr._wrote()
        self.assertEqual(tuple(wrote), gt)


if __name__ == '__main__':
    unittest.main()
