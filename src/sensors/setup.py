from setuptools import setup
import os
from glob import glob

package_name = 'sensors'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='ROS2 package for reading Pi Camera 3, BNO085 IMU, and AHT20 sensors',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_node = sensors.camera_node:main',
            'imu_node = sensors.imu_node:main',
            'temp_humidity_node = sensors.temp_humidity_node:main',
        ],
    },
)