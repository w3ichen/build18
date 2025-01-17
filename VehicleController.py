import numpy as np

class VehicleController:
    def __init__(self, R, c):
        self.R = R
        self.c
    
        # Thrust 1, Thrust 2, Thrust 3
        # Front, back left, back right
        # Y is pointed forwards
        # Fz = np.array([1,1,1])
        Tx = np.array([R, -R/2, -R/2])
        Ty = np.array([0, R * np.sqrt(3) / 2, -R * np.sqrt(3) / 2])
        self.M = np.array([Tx, Ty])
        self.Minv = np.inv(self.M)
        self.motor_pins = [MOTOR1, MOTOR2, MOTOR3]
        self.max_torque = 1

    def compute_motor_percentages(self, x, y):
       target = np.array([x,y])
       commands = self.Minv @ target
       return commands
    
    def control_motors(self, x, y):
        commands = compute_motor_percentages(x,y)
        for i in range(3):
            command = commands[i]
            if command > 100: command = 100
            if command < -100: command = -100
            if i > 0:
                c.drive_forward(self.motor_pins[i], command)
            else:
                c.drive_reverse(self.motor_pins[i], command)
    
