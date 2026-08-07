cd ~/Documents/2_ros2_prj/pendulum_ws
# colcon build --symlink-install
colcon build --packages-select description_robot
source install/setup.bash

# unset MESA_LOADER_DRIVER_NAME

# ros2 launch description_robot gazebo.launch.py