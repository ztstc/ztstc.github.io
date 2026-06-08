# ROS1 vs ROS2 迁移指南

本指南帮助初学者理解ROS1和ROS2的主要区别，以及如何将ROS1代码迁移到ROS2 Humble。

## 目录

1. 核心架构差异

2. 编程API变化

3. 构建系统

4. Launch文件

5. 消息和服务

6. 迁移检查清单

---

## 核心架构差异

### ROS1特点

- **单主节点\(Master\)**: 所有节点必须连接到中央ROS Master

- **同步通信**: 基于TCP/UDP，依赖于单点Master

- **实时性有限**: 不是实时操作系统

### ROS2特点

- **分布式架构**: 无中央Master，基于DDS\(Data Distribution Service\)

- **异步通信**: 基于发布\-订阅模型，支持多种通信中间件

- **实时性支持**: 可支持硬实时应用

- **更好的可扩展性**: 支持多机器协作

---

## 编程API变化

### 1\. 节点初始化

**ROS1:**

\#include \<ros/ros\.h\>



int main\(int argc, char\*\* argv\) \{

ros::init\(argc, argv, "my\_node"\);

ros::NodeHandle nh;



// 创建发布者

ros::Publisher pub = nh\.advertise\<std\_msgs::String\>\("chatter", 10\);



ros::spin\(\);

return 0;

\}

**ROS2:**

\#include \<rclcpp/rclcpp\.hpp\>

\#include \<std\_msgs/msg/string\.hpp\>



int main\(int argc, char\* argv\[\]\) \{

rclcpp::init\(argc, argv\);

auto node = std::make\_shared\<rclcpp::Node\>\("my\_node"\);



// 创建发布者

auto pub = node\-\>create\_publisher\<std\_msgs::msg::String\>\("chatter", 10\);



rclcpp::spin\(node\);

rclcpp::shutdown\(\);

return 0;

\}

### 2\. 发布者/订阅者

**ROS1:**

// 发布

ros::Publisher pub = nh\.advertise\<std\_msgs::String\>\("topic", 10\);

std\_msgs::String msg;

msg\.data = "Hello";

pub\.publish\(msg\);



// 订阅

void callback\(const std\_msgs::String::ConstPtr\& msg\) \{

ROS\_INFO\("I heard: \[%s\]", msg\-\>data\.c\_str\(\)\);

\}

ros::Subscriber sub = nh\.subscribe\("topic", 10, callback\);

**ROS2:**

// 发布

auto pub = node\-\>create\_publisher\<std\_msgs::msg::String\>\("topic", 10\);

auto msg = std::make\_shared\<std\_msgs::msg::String\>\(\);

msg\-\>data = "Hello";

pub\-\>publish\(\*msg\);



// 订阅

auto sub = node\-\>create\_subscription\<std\_msgs::msg::String\>\(

"topic", 10,

\[\]\(const std\_msgs::msg::String::SharedPtr msg\) \{

RCLCPP\_INFO\(node\-\>get\_logger\(\), "I heard: \[%s\]", msg\-\>data\.c\_str\(\)\);

\}\);

### 3\. 服务/客户端

**ROS1:**

// 服务

bool serviceCallback\(example\_pkg::MyService::Request\& req,

example\_pkg::MyService::Response\& res\) \{

res\.result = req\.input \* 2;

return true;

\}

ros::ServiceServer server = nh\.advertiseService\("service", serviceCallback\);



// 客户端

example\_pkg::MyService srv;

srv\.request\.input = 5;

ros::service::call\("service", srv\);

**ROS2:**

// 服务

auto callback = \[\]\(const std::shared\_ptr\<example\_pkg::srv::MyService::Request\> req,

std::shared\_ptr\<example\_pkg::srv::MyService::Response\> res\) \{

res\-\>result = req\-\>input \* 2;

\};

auto server = node\-\>create\_service\<example\_pkg::srv::MyService\>\("service", callback\);



// 客户端

auto client = node\-\>create\_client\<example\_pkg::srv::MyService\>\("service"\);

auto request = std::make\_shared\<example\_pkg::srv::MyService::Request\>\(\);

request\-\>input = 5;

auto result = client\-\>async\_send\_request\(request\);

### 4\. 日志记录

**ROS1:**

ROS\_DEBUG\("Debug message"\);

ROS\_INFO\("Info message"\);

ROS\_WARN\("Warning message"\);

ROS\_ERROR\("Error message"\);

ROS\_FATAL\("Fatal message"\);

**ROS2:**

RCLCPP\_DEBUG\(node\-\>get\_logger\(\), "Debug message"\);

RCLCPP\_INFO\(node\-\>get\_logger\(\), "Info message"\);

RCLCPP\_WARN\(node\-\>get\_logger\(\), "Warning message"\);

RCLCPP\_ERROR\(node\-\>get\_logger\(\), "Error message"\);

RCLCPP\_FATAL\(node\-\>get\_logger\(\), "Fatal message"\);

### 5\. 参数管理

**ROS1:**

ros::NodeHandle nh\("\~"\);

std::string param\_value;

nh\.getParam\("param\_name", param\_value\);

nh\.setParam\("param\_name", "new\_value"\);

**ROS2:**

auto param = node\-\>declare\_parameter\("param\_name", "default\_value"\);

auto param\_value = node\-\>get\_parameter\("param\_name"\)\.as\_string\(\);

node\-\>set\_parameter\(rclcpp::Parameter\("param\_name", "new\_value"\)\);

---

## 构建系统

### ROS1 CMakeLists\.txt

cmake\_minimum\_required\(VERSION 2\.8\.3\)

project\(example\_pkg\)



find\_package\(catkin REQUIRED COMPONENTS roscpp std\_msgs\)



catkin\_package\(\)



include\_directories\(include $\{catkin\_INCLUDE\_DIRS\}\)



add\_executable\(my\_node src/my\_node\.cpp\)

target\_link\_libraries\(my\_node $\{catkin\_LIBRARIES\}\)

### ROS2 CMakeLists\.txt

cmake\_minimum\_required\(VERSION 3\.8\)

project\(example\_pkg\)



if\(NOT CMAKE\_CXX\_STANDARD\)

set\(CMAKE\_CXX\_STANDARD 17\)

endif\(\)



find\_package\(ament\_cmake REQUIRED\)

find\_package\(rclcpp REQUIRED\)

find\_package\(std\_msgs REQUIRED\)



add\_executable\(my\_node src/my\_node\.cpp\)

target\_include\_directories\(my\_node PUBLIC include\)

ament\_target\_dependencies\(my\_node rclcpp std\_msgs\)



install\(TARGETS my\_node

DESTINATION lib/$\{PROJECT\_NAME\}\)



ament\_package\(\)

---

## Launch文件

### ROS1 \.launch \(XML格式\)

\<?xml version="1\.0"?\>

\<launch\>

\<arg name="use\_sim\_time" default="false"/\>



\<node pkg="example\_pkg" type="my\_node" name="my\_node" output="screen"\>

\<param name="param\_name" value="param\_value"/\>

\<remap from="input" to="output"/\>

\</node\>

\</launch\>

### ROS2 \.launch\.py \(Python格式\)

from launch import LaunchDescription

from launch\_ros\.actions import Node

from launch\.substitutions import LaunchConfiguration

from launch\.actions import DeclareLaunchArgument



def generate\_launch\_description\(\):

use\_sim\_time = LaunchConfiguration\('use\_sim\_time', default='false'\)



return LaunchDescription\(\[

DeclareLaunchArgument\(

'use\_sim\_time',

default\_value='false',

description='Use simulation \(Gazebo\) clock'

\),



Node\(

package='example\_pkg',

executable='my\_node',

name='my\_node',

output='screen',

parameters=\[\{'param\_name': 'param\_value'\}\],

remappings=\[\('input', 'output'\)\]

\)

\]\)

---

## 消息和服务

### ROS1 消息定义 \(\.msg\)

\# 文件: msg/MyMessage\.msg

string name

int32 age

float64 score

### ROS2 消息定义 \(\.msg\)

与ROS1相同，但在CMakeLists\.txt中的配置不同：

**ROS1:**

find\_package\(catkin REQUIRED COMPONENTS message\_generation std\_msgs\)

add\_message\_files\(FILES MyMessage\.msg\)

generate\_messages\(DEPENDENCIES std\_msgs\)

catkin\_package\(CATKIN\_DEPENDS message\_runtime\)

**ROS2:**

find\_package\(rosidl\_default\_generators REQUIRED\)

rosidl\_generate\_interfaces\($\{PROJECT\_NAME\}

"msg/MyMessage\.msg"

\)

ament\_package\(\)

---

## 迁移检查清单

### 代码级别

- 替换 `#include <ros/ros.h>` 为 `#include <rclcpp/rclcpp.hpp>`

- 更改 `ros::NodeHandle` 为 `rclcpp::Node`

- 更新发布者创建方式

- 更新订阅者创建和回调方式

- 更新服务创建和调用方式

- 替换所有日志调用（ROS\_INFO → RCLCPP\_INFO）

- 更新参数管理代码

- 替换 `ros::spin()` 为 `rclcpp::spin()`

### 配置文件

- 更新 CMakeLists\.txt（catkin → ament\_cmake）

- 更新 package\.xml（格式版本 1 → 2）

- 转换所有 \.launch 文件为 \.launch\.py

### 构建和测试

- 确保 C\+\+ 标准 ≥ 17

- 使用 `colcon build` 代替 `catkin_make`

- 检查所有依赖项都已安装

---

## 常见问题解答

**Q: 为什么ROS2没有Master？**
A: ROS2使用DDS中间件，支持分布式发现，不需要单点Master。

**Q: ROS2性能更好吗？**
A: 是的，DDS提供了更低的延迟和更高的吞吐量。

**Q: 我可以混合使用ROS1和ROS2吗？**
A: 可以，通过 `ros1_bridge` 包实现，但不推荐用于生产环境。

**Q: 学习ROS2需要多长时间？**
A: 如果你已了解ROS1，通常2\-4周即可掌握主要概念。

---

## 参考资源

- [ROS2官方迁移指南](https://docs.ros.org/en/humble/The-ROS2-Project/Contributing/Migration-Guide.html)

- [ROS2官方文档](https://docs.ros.org/en/humble/)

- [rclcpp API文档](https://docs.ros2.org/latest/api/rclcpp/)

- [ROS Discourse论坛](https://discourse.ros.org/)



