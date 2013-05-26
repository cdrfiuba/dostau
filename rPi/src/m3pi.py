from protocol import CMDS, LEFT, RIGHT


class M3pi:
    """
    This class implements the low lever communication protocol between the
    high level controller and the 3pi robot.
    """

    def __init__(self, transport):
        """
        :param transport: The physical transport layer. It should implement the
            open and write methods.
        """
        self.transport = transport

    def _set_motor_speed(self, motor, speed):
        """
        Sets the speed of any motor.

        :param motor: The motor.
        :type motor: int
        :param speed: A normalised number -1.0 - 1.0 represents the full range.
        :type speed: float
        """
        if motor not in [1, 2]:
            raise ValueError("Invalid motor index")

        mot = 'M' + str(motor) + '_'
        if speed >= 0:
            mot += 'FORWARD'
        else:
            mot += 'BACKWARD'

        self.transport.write([CMDS[mot], 0x7f * abs(speed)])

    def reset(self):
        """ Force a hardware reset of the 3pi."""
        raise NotImplementedError("The reset pin of the 3pi is not accesible.")

    def left_motor(self, speed):
        """
        Directly control the speed and direction of the left motor.

        :param speed: A normalised number -1.0 - 1.0 represents the full range.
        :type speed: float.
        """
        self._set_motor_speed(LEFT, speed)

    def right_motor(self, speed):
        """
        Directly control the speed and direction of the right motor.

        :param speed: A normalised number -1.0 - 1.0 represents the full range.
        :type speed: float.
        """
        self._set_motor_speed(RIGHT, speed)

    def straight(self, speed):
        """
        Sets both motors at the same speed.
        :param speed: A normalised number -1.0 - 1.0 represents the full range.
        :type speed: float.
        """
        self._set_motor_speed(RIGHT, speed)
        self._set_motor_speed(LEFT, speed)

    def left(self, speed):
        """
        Drive left motor backwards and right motor forwards at the same speed
        to turn left on the spot.

        :param speed: A normalised number 0 - 1.0 represents the full range.
        :type speed: float
        """
        self._set_motor_speed(RIGHT, speed)
        self._set_motor_speed(LEFT, -speed)

    def right(self, speed):
        """
        Drive right motor backwards and left motor forwards at the same speed
        to turn right on the spot.

        :param speed: A normalised number 0 - 1.0 represents the full range.
        :type speed: float
        """
        self._set_motor_speed(RIGHT, -speed)
        self._set_motor_speed(LEFT, speed)

    def stop(self):
        """ Stop both motors. """
        self._set_motor_speed(RIGHT, 0)
        self._set_motor_speed(LEFT, 0)

    def pot_voltage(self):
        """
        Read the voltage of the potentiometer on the 3pi.

        :returns: A normalized number representing the potentiometer value.
        :rtype: float
        """
        pass

    def battery(self):
        """
        Read the battery voltage on the 3pi.

        :returns: A number representing the current battery voltage.
        :rtype: float
        """
        pass

    def line_position(self):
        """ Read the position of the detected line.

        :returns: position as a normalised number -1.0 - 1.0 represents the
            full range:
            *  -1.0 means line is on the left, or the line has been lost
            *   0.0 means the line is in the middle
            *   1.0 means the line is on the right
        :rtype: float
        """
        pass

    def sensor_auto_calibrate(self):
        """
        Calibrate the sensors. This turns the robot left then right,
        looking for a line.
        """
        pass

    def calibrate(self):
        """
        Set calibration manually to the current settings.
        """
        self.transport.write([CMDS['PI_CALIBRATE']])

    def reset_calibration(self):
        """
        Clear the current calibration settings
        """
        self.transport.write([CMDS['LINE_SENSORS_RESET_CALIBRATION']])

    def PID_start(self, max_speed, a, b, c, d):
        self.transport.write([CMDS['SET_PID'], max_speed, a, b, c, d])

    def PID_stop(self):
        self.transport.write([CMDS['STOP_PID']])

    def locate(self, x, y):
        """
        Locate the cursor on the 8x2 LCD

        :param x: The horizontal position, from 0 to 7
        :type x: int
        :param y: The vertical position, from 0 to 1
        :type y: int
        """
        self.transport.write([CMDS['DO_LCD_GOTO_XY'], x, y])

    def cls(self):
        """
        Clear the LCD
        """
        self.transport.write([CMDS['DO_CLEAR']])


if __name__ == "__main__":
    car = m3pi()
