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
        print("WARNING: nav2_bringup package not found!")
        nav2_bringup_dir = None

    ekf_config_path = os.path.join(pkg_share, 'config', 'ekf.yaml')
    urdf_file = os.path.join(pkg_share, 'urdf', 'robot.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_path, {'use_sim_time': False}]  # ← added
    )

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': False  # ← added
        }]
    )

    launch_entities = [ekf_node, rsp_node]

    if nav2_bringup_dir:
        map_yaml_file = os.path.join(pkg_share, 'map', 'TES1.yaml')
        nav2_params_file = os.path.join(pkg_share, 'map', 'nav2_params.yaml')

        nav2_bringup_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': map_yaml_file,
                'params_file': nav2_params_file,
                'use_sim_time': 'false'  # ← lowercase
            }.items()
        )
        launch_entities.append(nav2_bringup_launch)

    return LaunchDescription(launch_entities)