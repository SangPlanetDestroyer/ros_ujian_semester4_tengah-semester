from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    cmd_vel_topic_arg = DeclareLaunchArgument(
        "cmd_vel_topic",
        default_value="/cmd_vel",
        description="ROS 2 cmd_vel topic to control the robot",
    )

    cmd_vel_topic = LaunchConfiguration("cmd_vel_topic")

    teleop_node = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="teleop_twist_keyboard",
        output="screen",
        emulate_tty=True,
        remappings=[("cmd_vel", cmd_vel_topic)],
    )

    return LaunchDescription(
        [
            cmd_vel_topic_arg,
            teleop_node,
        ]
    )
