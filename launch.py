#!/home/pi/build18/build18_env/bin/python

"""
Need to launch
1. sudo pigpiod (optional)
2. source build18_env/bin/activate (optional)
3. sudo ./launch.py
"""

import subprocess
from VehicleController import VehicleController

if __name__ == "__main__":
    # Start pigpiod
    print("Starting pigpiod...")
    subprocess.run(["sudo", "pigpiod"])
    print("Started pigpiod")

    print("Initializing VehicleController...")
    vehicle = VehicleController(R=77.5, verbose=False)
    print("Running vehicle...")
    vehicle.run()
