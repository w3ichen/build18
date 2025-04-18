# PHONY prevents is up to date check
.PHONY: build rosdep clean sensors

build:
	colcon build --symlink-install

sensors:
	colcon build --symlink-install --packages-select sensors

rosdep:
	rosdep install --from-paths src --ignore-src -y --rosdistro humble

clean:
	rm -rf build install log

frames:
	ros2 run tf2_tools view_frames

clean_frames:
	rm -r frames_*