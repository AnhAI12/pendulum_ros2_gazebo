import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = get_package_share_directory('description_robot')
    xacro_file = os.path.join(pkg_name, 'urdf','description.urdf.xacro')

    robot_description_raw = xacro.process_file(xacro_file).toxml()
    # Process xacro file to URDF XML text
    # doc = xacro.parse(open(xacro_file))
    # xacro.process_doc(doc)
    # robot_description_raw = doc.toxml()


    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
        'use_sim_time': True}] # add other parameters here if required
    )


    # 3. Launch Gazebo Harmonic (ros_gz_sim) with unpaused physics (-r)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
        launch_arguments={'gz_args': 'empty.sdf -r'}.items()
        )

    # 4. Spawn Entity in Gazebo Harmonic
    spawn_entity = Node(package='ros_gz_sim',
                        executable='create',
                        arguments=['-topic', 'robot_description',
                                '-name', 'my_bot'],
                        output='screen')
    # Node for public joint states to ROS 2
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=['joint_state_broadcaster'],
        output='screen'
    )
    # Node for force commands to Gazebo
    cart_effort_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=['cart_effort_controller'],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    # Run the node
    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
        cart_effort_controller_spawner,
        bridge
    ])


