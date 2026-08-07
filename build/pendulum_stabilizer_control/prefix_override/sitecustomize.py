import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/duyanh/Documents/2_ros2_prj/pendulum_ws/install/pendulum_stabilizer_control'
