#!/usr/bin/python

"""
https://www.underwaterthruster.com/blogs/knowledge/how-can-i-use-a-raspberry-pi-4b-to-send-a-pwm-signal-to-an-esc-to-control-an-underwater-thruster

Need to launch
1. sudo /usr/bin/pigpiod

PWM
Ranges: 50-100
Neutral: 75
Forward: 50-75
Backward: 75-100
"""

import pigpio
import time

# Motor pins
# PINS: Use Pins 12, 13, 18 and 19
MOTOR1 = 12
MOTOR2 = 13
MOTOR3 = 18

class MotorController:
    def __init__(self):
        self.pi = pigpio.pi()  # create pigpio object

        # PWM CONSTANTS
        self.PWM_FREQUENCY = 50  # define the PWM frequency in Hz
        self.PWM_range = 1000
        self.PWM_NEUTRAL = 75  # Off state

        # Init the pins
        self.init_motor_pin(MOTOR1)
        self.init_motor_pin(MOTOR2)
        self.init_motor_pin(MOTOR3)

    def init_motor_pin(self, pin):
        self.pi.set_mode(pin, pigpio.OUTPUT)  # Set the GPIO port to output mode
        self.pi.set_PWM_frequency(pin, self.PWM_FREQUENCY)  # set PWM frequency
        self.pi.set_PWM_range(pin, self.PWM_range)  # set range 1000
        self.pi.set_PWM_dutycycle(pin, self.PWM_NEUTRAL)  # set PWM duty cycle to neutral
        print(f"Initialized pin {pin}")

    def drive_forward(self, pin, speed):
        """
        :param speed: value from 0-100
        Positive rotation 7.5%-10% duty cycle, the larger the duty cycle, the faster the positive rotation speed
        """
        # Map speed (0-100) to 75-100
        pwm = 75 + (speed / 100) * 25
        self.pi.set_PWM_dutycycle(pin, pwm)
        print(f"Forward: pin={pin}, pwm={pwm}")
    
    def drive_reverse(self, pin, speed):
        """
        :param speed: value from 0-100
        Reverse The closer the duty cycle is to 5%, the faster the reversal speed is
        """
        pwm = 75 - (speed / 100) * 25
        self.pi.set_PWM_dutycycle(pin, pwm)
        print(f"Reverse: pin={pin}, pwm={pwm}")


if __name__ == "__main__":
    controller = MotorController()
    controller.drive_forward(MOTOR1, 100)
    time.sleep(3)
    controller.drive_forward(MOTOR1, 0)