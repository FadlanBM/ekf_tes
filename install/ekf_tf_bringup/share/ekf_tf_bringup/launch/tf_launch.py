from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('ekf_tf_bringup')
    
    ekf_config_path = os.path.join(pkg_share, 'config', 'ekf.yaml')
    
    # Path to the URDF file
    urdf_file = os.path.join(
        get_package_share_directory('ekf_tf_bringup'),
        'urdf',
        'robot.urdf'
    )
    
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Static transform: map -> odom (digunakan jika tidak ada SLAM/AMCL yang aktif)
    map_to_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='map_to_odom',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )

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

    # Nav2 Map Server nodes
    map_yaml_file = os.path.join(pkg_share, 'map', 'TES.yaml')
    nav2_params_file = os.path.join(pkg_share, 'map', 'nav2_params.yaml')

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[nav2_params_file, {'yaml_filename': map_yaml_file}]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        output='screen',
        parameters=[{'use_sim_time': False},
                    {'autostart': True},
                    {'node_names': ['map_server']}]
    )

    return LaunchDescription([
        map_to_odom,
        ekf_node,
        rsp_node,
        map_server_node,
        lifecycle_manager_node
    ])
