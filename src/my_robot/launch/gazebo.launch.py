from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package_name = "my_robot"
    package_share = Path(get_package_share_directory(package_name))
    xacro_path = package_share / "description" / "urdf" / "robot.xacro"
    urdf_path = package_share / "description" / "urdf" / "robot.urdf"
    world_path = package_share / "worlds" / "empty.world"

    robot_description = Command(["xacro ", str(xacro_path)])

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
            )
        ),
        launch_arguments={"gz_args": f"-r {world_path}"}.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_robot",
        output="screen",
        arguments=[
            "-name",
            package_name,
            "-file",
            str(urdf_path),
            "-x",
            "0.0",
            "-y",
            "0.0",
            "-z",
            "0.08",
        ],
    )

    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="clock_bridge",
        output="screen",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
    )

    cmd_vel_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="cmd_vel_bridge",
        output="screen",
        arguments=["/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist"],
    )

    imu_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="imu_bridge",
        output="screen",
        arguments=["/imu@sensor_msgs/msg/Imu[gz.msgs.IMU"],
    )

    return LaunchDescription(
        [
            gz_sim,
            robot_state_publisher,
            spawn_robot,
            clock_bridge,
            cmd_vel_bridge,
            imu_bridge,
        ]
    )
