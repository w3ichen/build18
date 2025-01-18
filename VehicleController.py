import numpy as np
from MotorController import MAX_SPEED_1_MOTOR, MAX_SPEED_2_MOTORS, MotorController, MOTOR1, MOTOR2, MOTOR3
from Joystick import Joystick
import sys
import time

class VehicleController:
    def __init__(self, R, verbose=False):
        self.R = R
        self.verbose = verbose
        self.motor_controller = MotorController(verbose=False)
    
        # Thrust 1, Thrust 2, Thrust 3
        # Front, back left, back right
        # Y is pointed forwards
        # Fz = np.array([1,1,1])
        Tx = np.array([R, -R/2, -R/2])
        Ty = np.array([0, R * np.sqrt(3) / 2, -R * np.sqrt(3) / 2])
        self.M = np.array([Tx, Ty])
        self.Minv = np.linalg.pinv(self.M)
        self.motor_pins = [MOTOR1, MOTOR2, MOTOR3]
        self.max_torque = 1

        # Init the joystick
        self.joystick = Joystick()

        # Manual control of status led
        self.set_ACT_led_trigger("none")

    def compute_motor_percentages(self, x, y):
       target = np.array([x,y])
       commands = self.Minv @ target
       return commands
    
    def control_motors(self, x, y):
        commands = self.compute_motor_percentages(x,y)
        for i in range(3):
            command = commands[i]
            if command > 100: 
                command = 100
            if command < -100: 
                command = 100

            if i > 0:
                self.motor_controller.drive_forward(self.motor_pins[i], command)
            else:
                self.motor_controller.drive_reverse(self.motor_pins[i], command)
    
    def read_joystick(self):
        btn = self.joystick.read_joy_btn()
        x = self.joystick.read_joy_x()
        y = self.joystick.read_joy_y()
        return btn, x, y
    
    @staticmethod
    def set_ACT_led_trigger(trigger):
        # Activity led trigger
        with open('/sys/class/leds/ACT/trigger', 'w') as f:
            f.write(trigger)

    @staticmethod
    def set_ACT_led_brightness(value):
        # Activity led brightness
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write(str(value))

    def run(self):
        print("Running motor, CTRL+C to stop!")
        while True:
            # Read joy
            btn, x, y = self.read_joystick()
            status_led_on = False # False will blink it, assume user signal so blink
            
            if btn:
                print("STOP")
                self.motor_controller.stop_all_motors()
            elif x > 60:
                # All up
                if self.verbose: print("Driving backwards")
                speed = ((x - 50)/50) * 100
                speed = min(speed, MAX_SPEED_2_MOTORS)
                self.motor_controller.drive_up(speed)
            elif x < 40:
                # All down
                if self.verbose: print("Driving forward")
                speed = ((50 - x)/50) * 100
                speed = min(speed, MAX_SPEED_2_MOTORS)
                self.motor_controller.drive_down(speed)
            elif y > 60:
                # Turn left
                if self.verbose: print("Turning left")
                speed = ((y - 50)/50) * 100
                speed = min(speed, MAX_SPEED_1_MOTOR)
                self.motor_controller.drive_reverse(MOTOR1, speed*(2/3))
                self.motor_controller.drive_reverse(MOTOR3, speed)
                self.motor_controller.drive_forward(MOTOR2, speed)
            elif y < 40:
                # Turn right
                if self.verbose: print("Turning right")
                speed = ((50 - y)/50) * 100
                speed = min(speed, MAX_SPEED_1_MOTOR)
                self.motor_controller.drive_reverse(MOTOR1, speed)
                self.motor_controller.drive_reverse(MOTOR3, speed*(2/3))
                self.motor_controller.drive_forward(MOTOR2, speed)
            else:
                # At rest
                if self.verbose: print("At rest")
                self.motor_controller.stop_all_motors()
                status_led_on = True # No user trigger, keep on

            self.set_ACT_led_brightness(int(status_led_on)) # Turn on or off led to blink it
            time.sleep(0.1) # Sleep
            # Have the led on when program is running
            self.set_ACT_led_brightness(1) 

            if not self.verbose: 
                # If not verbose, print dot for quality of life
                print(".", end="")
                sys.stdout.flush()
                

import atexit

def cleanup():
    print("="*40)
    print("Exiting VehicleController...")
    print("="*40)
    # Turn off ACT led on exit to indicate program is not running!
    VehicleController.set_ACT_led_brightness(0)

# Register the cleanup function
atexit.register(cleanup)
