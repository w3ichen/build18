# Run camera node
ros2 run sensors camera_node

# Run IMU node
ros2 run sensors imu_node

# Run temperature/humidity node
ros2 run sensors temp_humidity_node

ros2 launch sensors all_sensors.launch.py

# Build sensors package
make sensors