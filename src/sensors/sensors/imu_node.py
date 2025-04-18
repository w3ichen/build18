#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, MagneticField
from diagnostic_msgs.msg import DiagnosticStatus

import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR
)
from adafruit_bno08x.i2c import BNO08X_I2C

class BNO085Node(Node):
    def __init__(self):
        super().__init__('imu_node')
        
        # Declare parameters
        self.declare_parameter('frame_id', 'imu_frame')
        self.declare_parameter('i2c_frequency', 800000)  # Recommended to use 800kHz for RPi
        self.declare_parameter('update_rate', 50.0)      # Hz
        
        # Get parameter values
        self.frame_id = self.get_parameter('frame_id').value
        self.i2c_frequency = self.get_parameter('i2c_frequency').value
        self.update_rate = self.get_parameter('update_rate').value
        
        # Create publishers for the various topics
        self.imu_pub = self.create_publisher(Imu, 'imu/data', 10)
        self.mag_pub = self.create_publisher(MagneticField, 'imu/mag', 10)
        self.status_pub = self.create_publisher(DiagnosticStatus, 'imu/status', 10)
        
        # Initialize sensor
        self.get_logger().info(f'Initializing BNO085 with I2C frequency {self.i2c_frequency} Hz')
        try:
            i2c = busio.I2C(board.SCL, board.SDA, frequency=self.i2c_frequency)
            self.bno = BNO08X_I2C(i2c)
            self.get_logger().info('BNO085 sensor initialized')
        except Exception as e:
            self.get_logger().error(f'Failed to initialize BNO085 sensor: {str(e)}')
            # Try a different approach with a timeout setting
            self.get_logger().info('Trying alternative initialization with timeout')
            try:
                i2c = busio.I2C(board.SCL, board.SDA, frequency=self.i2c_frequency, timeout=1000)
                self.bno = BNO08X_I2C(i2c)
                self.get_logger().info('BNO085 sensor initialized with timeout setting')
            except Exception as e:
                self.get_logger().error(f'Failed alternate initialization: {str(e)}')
                raise
        
        # Enable the desired features
        self.bno.enable_feature(BNO_REPORT_ACCELEROMETER)
        self.bno.enable_feature(BNO_REPORT_GYROSCOPE)
        self.bno.enable_feature(BNO_REPORT_MAGNETOMETER)
        self.bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
        
        # Create timer for regular publishing
        timer_period = 1.0 / self.update_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Variables for covariance matrices
        # If covariance is unknown, it should be filled with zeros
        # If data element is unavailable, first element should be -1
        self.linear_acceleration_cov = [0.0] * 9  # Covariance unknown
        self.angular_velocity_cov = [0.0] * 9     # Covariance unknown
        self.orientation_cov = [0.0] * 9          # Covariance unknown
        self.magnetic_field_cov = [0.0] * 9       # Covariance unknown
        
        self.get_logger().info('BNO085 node initialized and running')
    
    def timer_callback(self):
        """Read data from the sensor and publish ROS2 messages"""
        try:
            # Get current time for message headers
            now = self.get_clock().now()
            
            # Create IMU message
            imu_msg = Imu()
            imu_msg.header.stamp = now.to_msg()
            imu_msg.header.frame_id = self.frame_id
            
            # Get quaternion orientation
            quat_i, quat_j, quat_k, quat_real = self.bno.quaternion
            imu_msg.orientation.w = quat_real
            imu_msg.orientation.x = quat_i
            imu_msg.orientation.y = quat_j
            imu_msg.orientation.z = quat_k
            
            # Set orientation covariance
            imu_msg.orientation_covariance = self.orientation_cov
            
            # Get angular velocity in rad/sec
            gyro_x, gyro_y, gyro_z = self.bno.gyro
            imu_msg.angular_velocity.x = gyro_x
            imu_msg.angular_velocity.y = gyro_y
            imu_msg.angular_velocity.z = gyro_z
            
            # Set angular velocity covariance
            imu_msg.angular_velocity_covariance = self.angular_velocity_cov
            
            # Get linear acceleration in m/s^2
            accel_x, accel_y, accel_z = self.bno.acceleration
            imu_msg.linear_acceleration.x = accel_x
            imu_msg.linear_acceleration.y = accel_y
            imu_msg.linear_acceleration.z = accel_z
            
            # Set linear acceleration covariance
            imu_msg.linear_acceleration_covariance = self.linear_acceleration_cov
            
            # Publish IMU message
            self.imu_pub.publish(imu_msg)
            
            # Create Magnetometer message
            mag_msg = MagneticField()
            mag_msg.header.stamp = now.to_msg()
            mag_msg.header.frame_id = self.frame_id
            
            # Get magnetic field in Tesla (BNO08x returns in microTesla)
            mag_x, mag_y, mag_z = self.bno.magnetic
            mag_msg.magnetic_field.x = mag_x * 1e-6  # Convert from microTesla to Tesla
            mag_msg.magnetic_field.y = mag_y * 1e-6
            mag_msg.magnetic_field.z = mag_z * 1e-6
            
            # Set magnetic field covariance
            mag_msg.magnetic_field_covariance = self.magnetic_field_cov
            
            # Publish Magnetometer message
            self.mag_pub.publish(mag_msg)
            
            # Create diagnostic status message to help with calibration monitoring
            status_msg = DiagnosticStatus()
            status_msg.name = "BNO085 IMU"
            status_msg.hardware_id = "BNO085"
            status_msg.level = DiagnosticStatus.OK
            status_msg.message = "IMU functioning normally"
            
            # Publish diagnostic status message
            self.status_pub.publish(status_msg)
            
        except Exception as e:
            self.get_logger().error(f'Error reading from BNO085: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    
    # Create and run node
    try:
        bno085_node = BNO085Node()
        rclpy.spin(bno085_node)
    except Exception as e:
        print(f'Exception in BNO085Node: {str(e)}')
    finally:
        # Clean up and shutdown
        rclpy.shutdown()

if __name__ == '__main__':
    main()