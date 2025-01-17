import time
import pigpio

# Motor pins
# PINS: Use Pins 12, 13, 18 and 19
MOTOR1 = 12
MOTOR2 = 13
MOTOR3 = 18
MOTORS = [MOTOR1, MOTOR2, MOTOR3]

class MotorController:
    """
    https://www.underwaterthruster.com/blogs/knowledge/how-can-i-use-a-raspberry-pi-4b-to-send-a-pwm-signal-to-an-esc-to-control-an-underwater-thruster
    PWM
    Ranges: 50-100
    Neutral: 75
    Forward: 50-75
    Backward: 75-100
    """
    def __init__(self, verbose=False):
        self.pi = pigpio.pi()  # create pigpio object
        self.verbose = verbose

        # PWM CONSTANTS
        self.PWM_FREQUENCY = 50  # define the PWM frequency in Hz
        self.PWM_range = 1000
        self.PWM_NEUTRAL = 75  # Off state

        # Init the pins
        self.init_motor_pin(MOTOR1)
        self.init_motor_pin(MOTOR2)
        self.init_motor_pin(MOTOR3)

    def init_motor_pin(self, motor_pin):
        self.pi.set_mode(motor_pin, pigpio.OUTPUT)  # Set the GPIO port to output mode
        self.pi.set_PWM_frequency(motor_pin, self.PWM_FREQUENCY)  # set PWM frequency
        self.pi.set_PWM_range(motor_pin, self.PWM_range)  # set range 1000
        self.pi.set_PWM_dutycycle(motor_pin, self.PWM_NEUTRAL)  # set PWM duty cycle to neutral
        if self.verbose: print(f"Initialized pin {motor_pin}")

    def drive_forward(self, motor_pin, speed):
        """
        :param speed: value from 0-100
        Positive rotation 7.5%-10% duty cycle, the larger the duty cycle, the faster the positive rotation speed
        """
        # Map speed (0-100) to 75-100
        pwm = 75 + (speed / 100) * 25
        self.pi.set_PWM_dutycycle(motor_pin, pwm)
        if self.verbose: print(f"Forward: pin={motor_pin}, speed={speed}, pwm={pwm}")
    
    def drive_reverse(self, motor_pin, speed):
        """
        :param speed: value from 0-100
        Reverse The closer the duty cycle is to 5%, the faster the reversal speed is
        """
        pwm = 75 - (speed / 100) * 25
        self.pi.set_PWM_dutycycle(motor_pin, pwm)
        if self.verbose: print(f"Reverse: pin={motor_pin}, speed={speed}, pwm={pwm}")

    def stop_motor(self, motor_pin):
        """
        Stop a motor
        """
        self.pi.set_PWM_dutycycle(motor_pin, self.PWM_NEUTRAL)
        if self.verbose: print(f"Stopped: pin={motor_pin}")
    
    def stop_all_motors(self):
        """
        Stop all motors
        """
        for motor_pin in MOTORS:
            self.stop_motor(motor_pin)
        if self.verbose: print(f"Stopped all motors")

    def drive_up(self, speed):
        """
        Drive all motors up at a certain speed
        """
        for motor_pin in MOTORS:
            self.drive_forward(motor_pin, speed)
        if self.verbose: print(f"Driving all motors up at speed={speed}")

    def drive_down(self, speed):
        """
        Drive all motors down at a certain speed
        """
        for motor_pin in MOTORS:
            self.drive_reverse(motor_pin, speed)
        if self.verbose: print(f"Driving all motors down at speed={speed}")


if __name__ == "__main__":
    controller = MotorController()
    controller.drive_forward(MOTOR1, 50)
    time.sleep(3)
    controller.drive_forward(MOTOR1, 0)