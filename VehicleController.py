import numpy as np
from MotorController import MotorController, MOTOR1, MOTOR2, MOTOR3
from Joystick import Joystick

import time

class VehicleController:
    def __init__(self, R):
        self.R = R
        self.motor_controller = MotorController()
    
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
        up = self.joystick.read_joy_btn()
        x = self.joystick.read_joy_x()
        y = self.joystick.read_joy_y()
        return up, x, y

    def run(self):
        print("Running motor, CTRL+C to stop!")
        while True:
            # Read joy
            up, x, y = self.read_joystick()
            if up:
                self.motor_controller.drive_up(100)
            else:
                self.motor_controller.drive_up(0)
                # self.control_motors(x,y)
            
            time.sleep(0.1)
