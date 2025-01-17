#!/home/pi/build18/build18_env/bin/python

"""
Need to launch
1. sudo /usr/bin/pigpiod
2. source build18_env/bin/activate (optional)
3. ./launch.py
"""

from VehicleController import VehicleController

if __name__ == "__main__":
    vehicle = VehicleController(R=77.5)
    vehicle.run()
