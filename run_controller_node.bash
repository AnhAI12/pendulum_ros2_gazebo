cd ~/Documents/2_ros2_prj/pendulum_ws
colcon build --packages-select pendulum_stabilizer_control
source install/setup.bash
ros2 run pendulum_stabilizer_control pendulum_controller_node