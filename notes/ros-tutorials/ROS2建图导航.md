# ROS2建图导航

## 环境配置

1. 首先下载建图cartographer和nav2包

```Plain Text
sudo apt install ros-humble-cartographer-ros ros-humble-nav2-bringup
```

2. 配置Cartographer参数文件

    - 找到配置模板：查看已安装的Cartographer包（如 `/opt/ros/humble/share/cartographer_ros/configuration_files/`），以 `demo_backpack_2d.lua` 等文件为模板。

    - 修改关键参数：将模板复制到你的项目目录，并修改Lua文件中的关键项：

        - `tracking_frame`、`published_frame`、`odom_frame`：修改为你的机器人底盘坐标系。

        - `provide_odom_frame`：根据你是否提供里程计设置为 `true` 或 `false`。

        - 雷达话题：将 `scan` 话题修改为你雷达发布的话题名。

3. 创建你的启动文件（Launch File）
基于模板（如`cartographer.launch.py`）创建一个新的launch文件，在其中：

    - 指定你修改后的Lua配置文件路径。

    - 设置正确的雷达话题名等参数。

4. 配置Nav2

    - 准备一个针对你小车的Nav2启动和参数配置文件。

    - 关键是通过 `nav2_params.yaml` 文件，正确配置 `controller_server`、`planner_server`、`behavior_server` 等服务器及其使用的插件。



复制Carto 文件到自己的包下

```Markdown
# 复制配置文件到你的功能包的config文件夹
cp /opt/ros/humble/share/cartographer/configuration_files/trajectory_builder_2d.lua ./config/my_robot_2d.lua
cp /opt/ros/humble/share/cartographer/configuration_files/map_builder.lua ./config/my_robot_map_builder.lua
```

包下创建一个launch文件夹`my_robot_cartographer.launch.py`

```Python
# my_robot_cartographer.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 1. 获取你的功能包的路径
    pkg_share = get_package_share_directory('my_slam_pkg') # 【重要】修改为你的包名

    # 2. 定义可传入的参数，例如配置文件名称
    configuration_basename = LaunchConfiguration('configuration_basename')
    declare_configuration_basename = DeclareLaunchArgument(
        'configuration_basename',
        default_value='my_robot_2d.lua', # 【重要】你的Lua配置文件名
        description='Name of lua configuration file for cartographer'
    )

    # 3. 启动Cartographer节点
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': False}], # 实体机器人设为False
        arguments=[
            '-configuration_directory', os.path.join(pkg_share, 'config'), # 【重要】指向你的config文件夹
            '-configuration_basename', configuration_basename
        ],
        # 可以重映射话题（如果你的话题名不是标准的）
        remappings=[
            ('scan', '/scan'),             # 假设你的雷达话题是 /scan
            ('odom', '/odom'),             # 假设你的里程计话题是 /odom
            ('imu', '/imu')                # 如果需要，映射IMU话题
        ]
    )

    # 4. 启动Cartographer的occupancy_grid_node（将子图转换为可用的地图）
    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='occupancy_grid_node',
        name='occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': False}],
        arguments=['-resolution', '0.05', '-publish_period_sec', '1.0'] # 地图分辨率和发布周期
    )

    # 5. （可选但推荐）启动静态TF广播，如果你的机器人URDF没发布 base_link->laser_link
    # 假设雷达坐标系叫 `laser_link`， 相对于底盘 `base_link` 有0.2米的高度
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        arguments=['0', '0', '0.2', '0', '0', '0', 'base_link', 'laser_link'] # x, y, z, roll, pitch, yaw, parent, child
    )

    return LaunchDescription([
        declare_configuration_basename,
        cartographer_node,
        occupancy_grid_node,
        static_tf_node, # 根据你的TF树情况决定是否添加
    ])
```



创建启动文件 \(`my_robot_nav2.launch.py`\)

这个文件负责“组装”整个导航系统。请将以下代码保存到你的功能包的 `launch` 目录，并修改三个关键位置：

```Python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, SetParameter

def generate_launch_description():# 【关键修改1】 设置你的功能包名
    pkg_name = 'my_slam_pkg'# 获取功能包路径
    pkg_share = get_package_share_directory(pkg_name)# 定义可传入的参数，如地图文件路径
    map_yaml_file = LaunchConfiguration('map')
    declare_map_arg = DeclareLaunchArgument('map',
        default_value=PathJoinSubstitution([pkg_share, 'maps', 'my_map.yaml']), # 【关键修改2】 你的地图路径
        description='Full path to map yaml file to load')# 设置全局参数：使用仿真时间？实体机器人设为False
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_arg = DeclareLaunchArgument('use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')# 设置参数文件路径
    params_file = LaunchConfiguration('params_file')
    declare_params_file_arg = DeclareLaunchArgument('params_file',
        default_value=PathJoinSubstitution([pkg_share, 'config', 'nav2_params.yaml']), # 【关键修改3】 你的参数文件路径
        description='Full path to the Nav2 parameters file')# 启动Nav2的核心主节点（它负责拉起所有服务器）
    nav2_launch_dir = get_package_share_directory('nav2_bringup')
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_launch_dir, '/launch', '/bringup_launch.py']),
        launch_arguments={'map': map_yaml_file,'use_sim_time': use_sim_time,'params_file': params_file,}.items())# （可选）启动Rviz2，方便可视化与交互
    rviz_config_file = PathJoinSubstitution([pkg_share, 'rviz', 'nav2_default_view.rviz'])
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen')return LaunchDescription([
        declare_map_arg,
        declare_use_sim_time_arg,
        declare_params_file_arg,
        SetParameter(name='use_sim_time', value=use_sim_time),
        nav2_bringup_launch,
        rviz_node, # 可选])
```



创建主参数文件 \(`config/nav2_params.yaml`\)

这是Nav2的“大脑”，决定了使用哪些算法插件以及如何配置它们。以下是一个最简化的、适用于差速轮式小车的配置，你需要重点关注注释中标记为【需修改】的部分：

```YAML
# 全局生命周期管理器配置
lifecycle_manager:
  ros__parameters:
    autostart: true
    node_names: ['controller_server', 'planner_server', 'behavior_server', 'bt_navigator', 'waypoint_follower', 'amcl']

# AMCL 定位服务器配置
amcl:
  ros__parameters:
    # 【需修改】设置你的机器人坐标系
    base_frame_id: "base_link"
    odom_frame_id: "odom"
    global_frame_id: "map"
    use_sim_time: false

    # 粒子滤波器参数 (可调整)
    min_particles: 500
    max_particles: 3000
    # 【需修改】设置你激光雷达的话题名
    scan_topic: "scan"

# 行为树导航器配置
bt_navigator:
  ros__parameters:
    global_frame: "map"
    robot_base_frame: "base_link"
    odom_topic: "odom"
    use_sim_time: false

# 控制器服务器 (负责路径跟踪和局部避障)
controller_server:
  ros__parameters:
    use_sim_time: false
    # 【需修改】设置你机器人底盘的帧ID
    frame_id: "base_link"

    # 指定使用的插件 (这里使用默认的DWB控制器)
    controller_plugins: ["FollowPath"]

    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      # 【需修改】设置你机器人底盘的帧ID， 并检查话题名
      robot_base_frame: "base_link"
      odom_topic: "odom"
      # 发布速度命令的话题， 需与你的底盘驱动订阅的话题一致
      cmd_vel_topic: "cmd_vel"

      # DWB规划器的具体参数 (可根据机器人性能调整)
      min_vel_x: -0.1
      max_vel_x: 0.3
      min_vel_theta: -0.5
      max_vel_theta: 0.5

# 规划器服务器 (负责全局路径规划)
planner_server:
  ros__parameters:
    use_sim_time: false
    expected_planner_frequency: 1.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5

# 行为服务器 (负责恢复行为，如清除代价地图、旋转)
behavior_server:
  ros__parameters:
    use_sim_time: false
    behavior_plugins: ["spin", "wait", "backup", "clear_costmap_service"]
    # ... 各行为参数

# 全局与局部代价地图配置 (定义障碍物信息源和地图大小)
global_costmap:
  global_costmap:
    ros__parameters:
      use_sim_time: false
      global_frame: "map"
      robot_base_frame: "base_link"
      update_frequency: 1.0
      publish_frequency: 1.0
      # 【需修改】设置你激光雷达的话题名， 作为障碍物源
      observation_sources: "scan"
      scan:
        data_type: "LaserScan"
        topic: "scan"
        marking: true
        clearing: true

local_costmap:
  local_costmap:
    ros__parameters:
      use_sim_time: false
      global_frame: "odom"
      robot_base_frame: "base_link"
      update_frequency: 5.0
      publish_frequency: 2.0
      width: 3.0
      height: 3.0
      # 【需修改】设置你激光雷达的话题名
      observation_sources: "scan"
      scan:
        data_type: "LaserScan"
        topic: "scan"
        marking: true
        clearing: true
```



## 建图

ros2 launch 这个文件

```Bash
ros2 launch my_slam_pkg my_robot_cartographer.launch.py
```

启动建图 可以在rviz2设置话题 看到map

推车推一会 然后 保存地图

```Plain Text
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

## 导航

ROS1的AMCL和Movebase被Nav2替代了 我们只需要启动nav2

```Bash
ros2 launch my_slam_pkg my_robot_nav2.launch.py
```

