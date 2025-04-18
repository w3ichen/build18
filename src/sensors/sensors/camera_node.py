#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from picamera2 import Picamera2

class PiCameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_node')
        
        # Create publisher for raw camera images
        self.publisher_ = self.create_publisher(Image, 'camera/image', 10)
        
        # Create parameters for camera configuration
        self.declare_parameter('frame_id', 'camera_frame')
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)
        self.declare_parameter('framerate', 15.0)
        
        # Get parameter values
        self.frame_id = self.get_parameter('frame_id').value
        self.width = self.get_parameter('width').value
        self.height = self.get_parameter('height').value
        self.framerate = self.get_parameter('framerate').value
        
        # Initialize the camera
        self.camera = Picamera2()
        
        # Configure the camera
        self.get_logger().info(f'Configuring camera: {self.width}x{self.height} @ {self.framerate} fps')
        video_config = self.camera.create_video_configuration(
            main={"size": (self.width, self.height), "format": "RGB888"}
        )
        self.camera.configure(video_config)
        
        # Set camera controls
        camera_controls = {}
        
        # Set framerate (convert to frame duration in microseconds)
        frame_duration = int((1.0 / self.framerate) * 1000000)
        camera_controls["FrameDurationLimits"] = (frame_duration, frame_duration)
        
        # Apply camera controls
        self.camera.set_controls(camera_controls)
        
        # Start the camera
        self.camera.start()
        self.get_logger().info('Camera started')
        
        # Create timer for publishing images
        timer_period = 1.0 / self.framerate  # seconds
        self.timer = self.create_timer(timer_period, self.capture_and_publish)
        
        self.get_logger().info('Pi Camera 3 node initialized')
        
    def capture_and_publish(self):
        """Capture an image from the camera and publish it to the ROS topic"""
        try:
            # Capture an image from the camera
            img = self.camera.capture_array()
            
            # Create Image message manually
            ros_img = Image()
            ros_img.header.stamp = self.get_clock().now().to_msg()
            ros_img.header.frame_id = self.frame_id
            ros_img.height = img.shape[0]
            ros_img.width = img.shape[1]
            ros_img.encoding = 'rgb8'
            ros_img.is_bigendian = False
            ros_img.step = img.shape[1] * 3  # 3 bytes per pixel
            ros_img.data = img.tobytes()
            
            # Publish the image
            self.publisher_.publish(ros_img)
            
        except Exception as e:
            self.get_logger().error(f'Error capturing image: {str(e)}')
    
    def __del__(self):
        """Cleanup when the node is destroyed"""
        if hasattr(self, 'camera'):
            self.camera.stop()
            self.get_logger().info('Camera stopped')

def main(args=None):
    rclpy.init(args=args)
    
    # Create and run the node
    node = PiCameraPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up and shut down
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()