import numpy as np
from MotorController import MotorController, MOTOR1, MOTOR2, MOTOR3
from Joystick import Joystick
import sys
import time

class VehicleController:
    def __init__(self, R, verbose=False):
        self.R = R
        self.verbose = verbose
        self.motor_controller = MotorController(verbose=verbose)
    
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

    def run(self):
        print("Running motor, CTRL+C to stop!")
        while True:
            # Read joy
            btn, x, y = self.read_joystick()
            
            if btn:
                print("STOP")
                self.motor_controller.stop_all_motors()
            elif x > 60:
                # All up
                if self.verbose: print("Driving up")
                speed = ((x - 50)/50) * 100
                self.motor_controller.drive_up(speed)
            elif x < 40:
                # All down
                if self.verbose: print("Driving down")
                speed = ((50 - x)/50) * 100
                self.motor_controller.drive_down(speed)
            elif y > 60:
                # Turn left
                if self.verbose: print("Turning left")
                speed = ((50 - y)/50) * 100
                self.motor_controller.stop_motor(MOTOR1)
                self.motor_controller.drive_forward(MOTOR3, speed)
            elif y < 40:
                # Turn right
                if self.verbose: print("Turning right")
                speed = ((y - 50)/50) * 100
                self.motor_controller.drive_forward(MOTOR1, speed)
                self.motor_controller.stop_motor(MOTOR3)
            else:
                # At rest
                self.motor_controller.stop_all_motors()

            time.sleep(0.1)
            if not self.verbose: 
                # If not verbose, print dot for quality of life
                print(".", end="")
                sys.stdout.flush()
                

