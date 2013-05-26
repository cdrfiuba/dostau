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
        gt = [0x54, 0x45, 0x53, 0x54]
        self.assertEqual(cmd_list, gt)

    def test_write(self):
        """
        Tests that I can read a value that was written to the transport.
        """
        test_cmd = [CMDS['M1_FORWARD']]
        self.tr.write(test_cmd)
        cmd = self.tr._wrote()
        self.assertEqual(test_cmd, cmd[0])


class Testm3pi(unittest.TestCase):
    """
    Tests the communication protocol with the 3pi robot.
    """

    def setUp(self):
        """ Excecuted before each test. """
        self.tr = TestTransport()
        self.robot = M3pi(self.tr)

    def tearDown(self):
        """ Excecuted after each test. """
        self.tr._clean()

    def _test_command(self, gt):
        """
        Helper function to test if the sent message was correct.
        Cleans the transport buffer after checking.

        :param gt: The expected message.
        :type gt: int list
        :returns: true of false
        :rtype: bool
        """
        wrote = self.tr._wrote()[0]
        self.assertEqual(tuple(wrote), gt)
        self.tr._clean()

    def test_set_motor_speed(self):
        """
        Tests that the set motor speed function sends the correct values.
        It should send the command stating the motor and direction and then the
        speed value in absolute value multiplied by 0x7f
        """
        self.robot._set_motor_speed(1, 1)
        self._test_command((CMDS['M1_FORWARD'], 0x7f * abs(1)))

        self.robot._set_motor_speed(2, 1)
        self._test_command((CMDS['M2_FORWARD'], 0x7f * abs(1)))
        
        self.robot._set_motor_speed(2, -0.5)
        self._test_command((CMDS['M2_BACKWARD'], int(0x7f * abs(-0.5))))
        
    def test_left_motor(self):
        """
        Tests if the correct motor index is used when calling the left motor
        wrapper.
        """
        self.robot.left_motor(-1)
        motor_index = self.tr._wrote()[0][0]
        self.assertEqual(CMDS['M2_BACKWARD'], motor_index)

    def test_right_motor(self):
        """
        Tests if the correct motor index is used when calling the right motor
        wrapper.
        """
        self.robot.right_motor(1)
        motor_index = self.tr._wrote()[0][0]
        self.assertEqual(CMDS['M1_FORWARD'], motor_index)

    def test_left(self):
        """
        left should turn left-wise in place (right motor going forward and the
        left backward.
        """
        self.robot.left(1)
        sent = self.tr._wrote()
        self.assertEqual([CMDS['M1_FORWARD'], 0x7f], sent[0])
        self.assertEqual([CMDS['M2_BACKWARD'], 0x7f], sent[1])

    def test_right(self):
        """
        left should turn right-wise in place (left motor going forward and the
        right backward.
        """
        self.robot.right(1)
        sent = self.tr._wrote()
        self.assertEqual([CMDS['M1_BACKWARD'], 0x7f], sent[0])
        self.assertEqual([CMDS['M2_FORWARD'], 0x7f], sent[1])

    def test_straight_forward(self):
        """
        The straight method should set both motors at the same speed, going
        forward in this test.
        """
        self.robot.straight(1)
        sent = self.tr._wrote()
        self.assertEqual([CMDS['M1_FORWARD'], 0x7f], sent[0])
        self.assertEqual([CMDS['M2_FORWARD'], 0x7f], sent[1])

    def test_straight_forward(self):
        """
        The straight method should set both motors at the same speed. Going
        backwards in this test.
        """
        self.robot.straight(-1)
        sent = self.tr._wrote()
        self.assertEqual([CMDS['M1_BACKWARD'], 0x7f], sent[0])
        self.assertEqual([CMDS['M2_BACKWARD'], 0x7f], sent[1])

    def test_stop(self):
        """
        The stop method should set both to 0 speed.
        """
        self.robot.stop()
        sent = self.tr._wrote()
        self.assertEqual([CMDS['M1_FORWARD'], 0], sent[0])
        self.assertEqual([CMDS['M2_FORWARD'], 0], sent[1])

    def test_PID_start(self):
        """
        Sets the PID controller. There is no documentation on the parameters
        for te PID_start function.
        """
        args = [1, 2, 3, 4, 5]
        self.robot.PID_start(*args)
        self.assertEqual(self.tr._wrote()[0], [CMDS['SET_PID']] + args)

    def test_PID_stop(self):
        """
        Sets the PID controller. There is no documentation on the parameters
        for te PID_start function.
        """
        self.robot.PID_stop()
        self.assertEqual(self.tr._wrote()[0], [CMDS['STOP_PID']])

    def test_reset(self):
        """ In dos-tau tere is no connection between the rPi and the 3pi reset
        pin. This method should raise an exception."""
        self.assertRaises(NotImplementedError, self.robot.reset)

    def test_calibrate(self):
        self.robot.calibrate()
        sent = self.tr._wrote()
        self.assertEqual(self.tr._wrote()[0], [CMDS['PI_CALIBRATE']])

    def test_reset_calibration(self):
        """ Resets te IR sensor calibration values. """
        self.robot.reset_calibration()
        sent = self.tr._wrote()
        self.assertEqual(self.tr._wrote()[0], [CMDS['LINE_SENSORS_RESET_CALIBRATION']])

    def test_locate(self):
        """ Moves the LCD cursor to a given prosition. """
        self.robot.locate(1, 1)
        sent = self.tr._wrote()
        self.assertEqual(sent[0], [CMDS['DO_LCD_GOTO_XY'], 1, 1])
        
    def test_clear(self):
        """ Clears the LCD screen. """
        self.robot.cls()
        self.assertEqual(self.tr._wrote()[0], [CMDS['DO_CLEAR']])


if __name__ == '__main__':
    unittest.main()
