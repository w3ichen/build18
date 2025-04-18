#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature, RelativeHumidity
from std_msgs.msg import Header

import time
import board
import adafruit_ahtx0

class AHT20Node(Node):
    def __init__(self):
        super().__init__('temp_humidity_node')
        
        # Create publishers
        self.temp_publisher = self.create_publisher(
            Temperature, 
            'temperature', 
            10)
        self.humidity_publisher = self.create_publisher(
            RelativeHumidity, 
            'humidity', 
            10)
        
        # Declare parameters
        self.declare_parameter('frame_id', 'temp_humidity_frame')
        self.declare_parameter('update_rate', 1.0)  # Hz
        
        # Get parameter values
        self.frame_id = self.get_parameter('frame_id').value
        update_rate = self.get_parameter('update_rate').value
        
        # Initialize the sensor
        try:
            i2c = board.I2C()  # uses board.SCL and board.SDA
            self.sensor = adafruit_ahtx0.AHTx0(i2c)
            self.get_logger().info('AHT20 sensor initialized successfully!')
        except Exception as e:
            self.get_logger().error(f'Failed to initialize AHT20 sensor: {str(e)}')
            raise
        
        # Create timer for regular readings
        self.timer = self.create_timer(1.0/update_rate, self.timer_callback)
        
        self.get_logger().info('AHT20 node is running')
    
    def timer_callback(self):
        try:
            # Read sensor data
            temperature_c = self.sensor.temperature
            relative_humidity = self.sensor.relative_humidity
            
            # Get current time for message headers
            current_time = self.get_clock().now().to_msg()
            
            # Create and publish temperature message
            temp_msg = Temperature()
            temp_msg.header = Header()
            temp_msg.header.stamp = current_time
            temp_msg.header.frame_id = self.frame_id
            temp_msg.temperature = temperature_c
            temp_msg.variance = 0.0  # Set to 0.0 if unknown
            
            self.temp_publisher.publish(temp_msg)
            
            # Create and publish humidity message
            humidity_msg = RelativeHumidity()
            humidity_msg.header = Header()
            humidity_msg.header.stamp = current_time
            humidity_msg.header.frame_id = self.frame_id
            humidity_msg.relative_humidity = relative_humidity / 100.0  # Convert to ratio (0.0-1.0)
            humidity_msg.variance = 0.0  # Set to 0.0 if unknown
            
            self.humidity_publisher.publish(humidity_msg)
            
            # Log data (for debugging)
            self.get_logger().debug(f'Temperature: {temperature_c:.1f}°C, Humidity: {relative_humidity:.1f}%')
            
        except Exception as e:
            self.get_logger().error(f'Error reading from AHT20 sensor: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    
    try:
        aht20_node = AHT20Node()
        rclpy.spin(aht20_node)
    except Exception as e:
        print(f'Exception in AHT20Node: {str(e)}')
    finally:
        # Clean up before exiting
        rclpy.shutdown()

if __name__ == '__main__':
    main()