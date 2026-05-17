import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('ekf_tf_bringup')
    
    try:
        nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    except Exception:
        print("WARNING: nav2_bringup package not found! Nav2 will not launch.")
        nav2_bringup_dir = None
    
    ekf_config_path = os.path.join(pkg_share, 'config', 'ekf.yaml')
    
    # Path to the URDF file
    urdf_file = os.path.join(
        pkg_share,
        'urdf',
        'robot.urdf'
    )
    
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Node Robot Localization: odom -> base_link
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_path]
    )

    # Robot State Publisher to publish transforms for wheels and lasers based on URDF
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Relay node to sync odometry timestamps
    odom_relay_node = Node(
        package='ekf_tf_bringup',
        executable='odom_time_relay',
        name='odom_time_relay',
        output='screen'
    )

    launch_entities = [ekf_node, rsp_node, odom_relay_node]

    # Nav2 Bringup Launch
    if nav2_bringup_dir:
        map_yaml_file = os.path.join(pkg_share, 'map', 'TES.yaml')
        nav2_params_file = os.path.join(pkg_share, 'map', 'nav2_params.yaml')

        nav2_bringup_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': map_yaml_file,
                'params_file': nav2_params_file,
                'use_sim_time': 'False',
                'use_composition': 'False'
            }.items()
        )
        launch_entities.append(nav2_bringup_launch)

    return LaunchDescription(launch_entities)
