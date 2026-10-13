from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    motor_node = Node(
        package='system_check',
        executable='motor_safety_ctrl'
    )
    robot_node = Node(
        package='system_check',
        executable='robot_safety_ctrl'
    )

    ld.add_action(motor_node)
    ld.add_action(robot_node)

    return ld