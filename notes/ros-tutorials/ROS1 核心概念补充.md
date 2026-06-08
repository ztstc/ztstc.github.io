# ROS1 核心概念补充

## 节点 / 话题 / 消息 / 参数 / Launch / 工作空间 / catkin\_make

> 环境假设：Ubuntu 20\.04 \+ ROS Noetic，已 `source /opt/ros/noetic/setup.bash`（或 `~/.bashrc` 自动 source）。
> 
> 

---

## 节点（node）：一个运行中的进程（executable）

### 1\.1 节点是什么

- **节点**就是一个正在运行的程序（进程），通常由你的包编译生成的可执行文件启动而来。

- 在 ROS1 中，节点通过 **ROS Master（roscore）** 协调互相发现（谁发布了什么话题、谁提供了什么服务等）。

### 1\.2 节点能做什么

- 发布（publish）消息到某个话题

- 订阅（subscribe）某个话题并接收消息

- 提供服务（service server）/调用服务（service client）

- 读写参数服务器（param server）

- 广播 TF（坐标变换）

### 1\.3 常用命令（实操）

```Bash
# 1) 启动 master（很多操作需要它）
roscore

# 2) 查看当前在线节点
rosnode list

# 3) 查看某个节点的详细信息（发布/订阅了哪些话题等）
rosnode info /talker
```

### 1\.4 关键理解

- “节点名”（如 `/talker`）≠ Linux 进程名，但对应某个进程的 ROS 身份。

- 同一可执行文件可以启动多个实例，只要 node name 不冲突（或用匿名名/namespace）。

---

## 话题（topic）：发布/订阅的消息通道（异步）

### 2\.1 话题是什么

- **话题**是一条“消息流通道”，采用**发布/订阅模型**。

- **异步**：发布者与订阅者不需要在同一时刻“请求\-响应”，发布者按频率发，订阅者收到就处理。

### 2\.2 一个话题包含什么信息

- 话题名字：例如 `/chatter`

- 消息类型：例如 `std_msgs/String`

- 发布者（publishers）列表

- 订阅者（subscribers）列表

### 2\.3 常用命令（实操）

```Bash
# 查看当前系统存在的话题
rostopic list

# 查看某个话题类型
rostopic type /chatter

# 查看话题详细信息（发布者/订阅者/类型）
rostopic info /chatter

# 打印话题内容（实时流）
rostopic echo /chatter

# 查看话题频率（是否稳定、是否过快）
rostopic hz /chatter
```

### 2\.4 队列（queue）是新手常忽略的点

- 发布/订阅代码里常见 `queue_size`（如 10）。

- 订阅者处理不过来时，队列满了会丢旧消息或新消息（取决于实现/缓冲策略），因此频率和处理耗时必须考虑。

---

## 消息（msg）：通信数据结构（如 std\_msgs/String）

### 3\.1 msg 是什么

- **消息**就是 ROS 话题/服务传输的数据结构。

- ROS 已内置很多常用消息： 

    - `std_msgs/String`、`std_msgs/Int32`

    - 机器人运动常用：`geometry_msgs/Twist`（速度）、`nav_msgs/Odometry`（里程计）

    - 传感器常用：`sensor_msgs/Image`、`sensor_msgs/LaserScan`

### 3\.2 查看消息定义（非常常用）

```Bash
# 查看某个消息类型的字段定义
rosmsg show std_msgs/String
rosmsg show geometry_msgs/Twist
```

### 3\.3 自定义 msg（概念预告）

当内置消息不够用，你可以在包内创建：

- `msg/YourType.msg` 然后在 `CMakeLists.txt` 与 `package.xml` 里声明生成规则。

> 新手建议：先熟练使用现成消息（Twist、Pose、Image…），等写到“数据结构确实不合适”再自定义。
> 
> 

---

## 参数（param）：运行时配置（可通过 launch/命令行设置）

### 4\.1 参数是什么

- 参数是运行时配置数据，存放于 ROS 的 **Parameter Server**（参数服务器）。

- 常用于： 

    - 配置算法参数（阈值、最大速度、topic 名称）

    - 配置节点运行频率（rate）、坐标系名称（frame\_id）

    - 配置传感器标定、路径等

### 4\.2 参数的数据类型

常见：`int`、`double`、`bool`、`string`、list、dict（YAML）

### 4\.3 常用命令（实操）

```Bash
# 列出所有参数
rosparam list

# 获取某个参数
rosparam get /use_sim_time

# 设置某个参数
rosparam set /my_param 123

# 删除某个参数
rosparam delete /my_param
```

### 4\.4 参数命名空间（namespace）与私有参数（\~）

- 全局参数：`/robot_name`

- 某节点私有参数：`~rate`

    - 写在 launch 的 `<node> ... <param .../> ... </node>` 内，通常就是该节点的私有参数

- 代码里读取私有参数常见写法： 

    - C\+\+：`ros::NodeHandle nh("~"); nh.param("rate", hz, 10);`

    - Python：`rospy.get_param("~rate", 10)`

---

## launch：一键启动多个节点 \+ 参数 \+ 重映射

### 5\.1 launch 是什么

- `roslaunch` 用一个 `.launch` 文件启动多个节点，并设置参数、命名空间、重映射等，属于 ROS1 的“工程化入口”。

### 5\.2 为什么新手要尽早用 launch

- 你不用手敲多个 `rosrun ...`

- 参数、topic 重映射都写文件里，可复用、可版本管理

- 方便团队协作：别人拉下代码就能 `roslaunch` 跑起来

### 5\.3 最小 launch 示例

```XML
<launch>
  <node pkg="hello_ros" type="talker_node" name="talker" output="screen">
    <param name="rate" value="5" />
  </node>

  <node pkg="hello_ros" type="listener_node" name="listener" output="screen" />
</launch>
```

启动：

```Bash
roslaunch hello_ros start.launch
```

### 5\.4 重映射（remap）：不改代码换话题名（高频用法）

示例：把 talker 发布的 `chatter` 改成 `chatter2`：

```XML
<node pkg="hello_ros" type="talker_node" name="talker" output="screen">
  <remap from="chatter" to="chatter2" />
</node>
```

验证：

```Bash
rostopic list
rostopic echo /chatter2
```

### 5\.5 namespace：让多机器人/多实例不打架

```XML
<launch>
  <group ns="robot1">
    <node pkg="hello_ros" type="talker_node" name="talker" />
  </group>

  <group ns="robot2">
    <node pkg="hello_ros" type="talker_node" name="talker" />
  </group>
</launch>
```

这样会出现两个节点：

- `/robot1/talker`

- `/robot2/talker`

---

## 工作空间（catkin\_ws）：你的所有包的集合

### 6\.1 工作空间是什么

- **工作空间**是你放 ROS 包（packages）并进行统一编译的地方。

- 典型结构（最常见）：

```Plain Text
catkin_ws/
  src/                # 你的所有 ROS packages 都放这里（源码）
  build/              # 构建中间产物（catkin_make 生成）
  devel/              # 开发环境产物：setup.bash、可执行文件等
```

### 6\.2 为什么要 source 工作空间

- `source ~/catkin_ws/devel/setup.bash` 会把你的“自定义包”加入环境： 

    - shell 能找到 `rosrun hello_ros ...`

    - `rospack find hello_ros` 能定位到包路径

    - `ROS_PACKAGE_PATH` 会包含 `~/catkin_ws/src`

### 6\.3 常用命令

```Bash
# 查包路径
rospack find hello_ros

# 查看 ROS 包依赖关系（可选）
rospack depends hello_ros
```

---

## catkin\_make：构建整个工作空间

### 7\.1 catkin\_make 在做什么

- `catkin_make` 是 ROS1（catkin）的经典构建入口，内部基于 CMake。

- 它会： 

    1. 扫描 `src/` 下所有 package

    2. 根据依赖顺序组织构建

    3. 把可执行文件、库、生成的消息等放到 `devel/`，中间产物放到 `build/`

### 7\.2 常用用法

```Bash
cd ~/catkin_ws
catkin_make
```

只编译某些目标（进阶）：

```Bash
catkin_make --pkg hello_ros
```

清理构建（简单粗暴）

```Bash
cd ~/catkin_ws
rm -rf build devel
catkin_make
```

### 7\.3 新手常见报错与含义

- **找不到头文件/库**：通常是依赖没装、或 `CMakeLists.txt` 没写 `find_package(...)` / `target_link_libraries(...)`

- **rosrun 找不到可执行文件**：没 `source devel/setup.bash`，或没成功编译出该 target

- **launch 里 type 找不到**：launch 中 `type=` 写错（应为编译生成的可执行文件名）

---

# 总结

---



