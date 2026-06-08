# VS Code 打造你的第一个 ROS包

## 从 0 到能跑（含中文、CMake、Copilot、Launch）

> 适用环境：Ubuntu 20\.04 \+ ROS Noetic（ROS1）
> 
> 目标：用 VS Code 完成 **工作区创建 → 新建 package → 写 C\+\+ 节点 → 编译 → launch 启动 → 参数/日志/常用调试**
> 
> 读完你将得到：一个可运行的 `hello_ros` 包（含 talker/listener 与 launch）。
> 
> 

---

```Bash
sudo apt update
sudo apt -y install git curl build-essential
```

---

## 安装 VS Code（推荐用 \.deb 或 apt）

### 1\.1 安装（推荐 apt 仓库方式）

如果你已经安装过 VS Code 可跳过。也可以使用官网下载 `.deb` 双击安装。

---

## VS Code 必装插件（中文 \+ ROS \+ CMake \+ Copilot）

打开 VS Code → 左侧扩展（Extensions）→ 搜索安装以下插件：

### 2\.1 中文汉化插件

- **Chinese \(Simplified\) \(简体中文\)**（Microsoft）

安装后按提示重启 VS Code 生效。

### 2\.2 ROS 插件（关键）**Robot Developer Extensions for ROS**

- **ROS**（Microsoft） 

    - 提供 ROS 包识别、launch 语法高亮、ROS 命令面板、环境切换等

### 2\.3 C/C\+\+ 与 CMake

- **C/C\+\+**（Microsoft）

- **CMake Tools**（Microsoft）

> ROS1 传统用 catkin \+ CMakeLists\.txt；这两插件有助于代码跳转、补全、构建配置等。
> 
> 

### 2\.4 GitHub Copilot

- **GitHub Copilot**

- （可选）**GitHub Copilot Chat**

> 需要你登录 GitHub 并拥有 Copilot 权限/订阅（或组织提供）。
> 
> 

你可以参考我的笔记获得免费的**GitHub Copilot Pro:**

[GitHub笔记](https://github.com/ztstc/note/blob/main/Git_GitHub_Copilot%E7%AC%94%E8%AE%B0/Git%20%26%20GitHub%20%26%20Copilot%E4%BD%BF%E7%94%A8%E6%8C%87%E5%BC%95.md)

---

## 安装编译链与 ROS 开发常用包（必做）

### 3\.1 catkin 与常用工具

```Bash
sudo apt update
sudo apt -y install python3-catkin-tools
```

> 说明：你也可以继续使用 catkin\_make（ROS1最常见）。
> 
> `catkin_tools` 更现代（`catkin build`），但本文先以 `catkin_make` 为主，确保新手最少踩坑。
> 
> 

### 3\.2 ROS C\+\+ 常用依赖

```Bash
sudo apt -y install ros-noetic-roscpp ros-noetic-std-msgs
```

---

## 创建你的 ROS 工作区（catkin\_ws）

### 4\.1 创建目录结构

```Bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
```

### 4\.2 设置环境（强烈建议写入 \~/\.bashrc）

```Bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 4\.3 验证工作区可用

```Bash
echo $ROS_PACKAGE_PATH
# 应包含 .../catkin_ws/src
```

---

## 用 VS Code 打开工作区（正确姿势）

### 5\.1 从终端启动 VS Code（推荐）

这样 VS Code 会继承 ROS 环境变量（新手最容易忽略）：

```Bash
cd ~/catkin_ws
code .
```

> 如果你从桌面图标直接打开 VS Code，有时 ROS 环境变量没有加载，会出现“找不到头文件 / 无法补全”等问题。
> 
> 

---

## 创建第一个 package（hello\_ros）

### 6\.1 在 src 下创建包

```Bash
cd ~/catkin_ws/src
catkin_create_pkg hello_ros roscpp std_msgs
```

生成结构大致如下：

```Plain Text
hello_ros/
  CMakeLists.txt
  package.xml
  src/
```

### 6\.2 让 VS Code 识别工程（建议）

回到工作区根目录编译一次（生成编译数据库/中间文件）：

```Bash
cd ~/catkin_ws
catkin_make
```

---

## 编写第一个节点：talker（发布者，C\+\+）

在 `~/catkin_ws/src/hello_ros/src/` 新建文件 `talker.cpp`：

```C++
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <sstream>

int main(int argc, char** argv)
{
  ros::init(argc, argv, "talker");
  ros::NodeHandle nh;

  ros::Publisher pub = nh.advertise<std_msgs::String>("chatter", 10);

  ros::Rate rate(10); // 10 Hz
  int count = 0;

  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    ss << "hello_ros says hi, count=" << count++;
    msg.data = ss.str();

    ROS_INFO_STREAM("Publishing: " << msg.data);

    pub.publish(msg);
    ros::spinOnce();
    rate.sleep();
  }

  return 0;
}
```

## **再写一个节点：listener（订阅者，C\+\+）**

新建 `listener.cpp`：

**catkin\_ws/src/hello\_ros/src/listener\.cpp**

```C++
#include <ros/ros.h>
#include <std_msgs/String.h>

void callback(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO_STREAM("I heard: " << msg->data);
}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe("chatter", 10, callback);

  ros::spin();
  return 0;
}
```

---

## **修改 CMakeLists\.txt：把两个节点编译出来（关键一步）**

打开 `~/catkin_ws/src/hello_ros/CMakeLists.txt`，找到并确保以下内容存在（按需插入即可）。

> 提示：catkin\_create\_pkg 生成的 CMakeLists 是模板，很多段落默认注释掉，需要你“取消注释/添加”。
> 
> 

在 `find_package(catkin REQUIRED COMPONENTS ...)` 中确保包含：

- `roscpp`

- `std_msgs`

并在文件合适的位置添加（通常在 `catkin_package()` 后面）：

**catkin\_ws/src/hello\_ros/CMakeLists\.txt**

```C++
cmake_minimum_required(VERSION 3.0.2)
project(hello_ros)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(talker_node src/talker.cpp)
target_link_libraries(talker_node ${catkin_LIBRARIES})

add_executable(listener_node src/listener.cpp)
target_link_libraries(listener_node ${catkin_LIBRARIES})
```

> 如果你的文件里已经有同名段落，避免重复；以“最终效果可编译”为准。
> 
> 

---

## **编译整个工作区**

回到工作区根目录：

bash

`cd ~/catkin_ws catkin_make`

编译成功后你会看到：

- 可执行文件生成在：`devel/lib/hello_ros/`

如果报错，优先检查：

- `CMakeLists.txt` 是否正确添加 `add_executable` 与 `target_link_libraries`

- 是否缺依赖：`sudo apt install ros-noetic-roscpp ros-noetic-std-msgs`

---

## **运行验证（不使用 launch）**

### **11\.1 终端 1：启动 roscore**

bash

`roscore`

### **11\.2 终端 2：运行 talker**

bash

`source ~/.bashrc rosrun hello_ros talker_node`

### **11\.3 终端 3：运行 listener**

bash

`source ~/.bashrc rosrun hello_ros listener_node`

你应看到：

- talker 持续 Publishing

- listener 持续 I heard

---

## **编写 launch：一条命令启动两个节点（ROS 入门必会）**

### **12\.1 创建 launch 目录和文件**

bash

`mkdir -p ~/catkin_ws/src/hello_ros/launch`

新建 `start.launch`：

**catkin\_ws/src/hello\_ros/launch/start\.launch**v1

```XML
<launch>
  <!-- 同时启动 talker 与 listener -->
  <node pkg="hello_ros" type="talker_node" name="talker" output="screen" />
  <node pkg="hello_ros" type="listener_node" name="listener" output="screen" />
</launch>
```

### **12\.2 使用 launch 启动**

bash

\`roscore

# 或者不手动开 roscore：roslaunch 会自动拉起 roscore（推荐）\`

推荐直接：

bash

`roslaunch hello_ros start.launch`

---

## **进一步：加一个参数（param）让程序更像“工程”**

我们让 talker 支持参数 `~rate` 控制发布频率。

### **13\.1 修改 talker\.cpp（读取参数）**

将 `ros::Rate rate(10);` 改为：

**catkin\_ws/src/hello\_ros/src/talker\.cpp**

```C++
int hz;
  nh.param("rate", hz, 10); // 参数名 rate，默认 10
  ros::Rate rate(hz);
```

完整逻辑：如果 launch 或命令行没有设置参数，就用默认 10Hz。

### **13\.2 在 launch 中设置参数**

更新 `start.launch`：

**catkin\_ws/src/hello\_ros/launch/start\.launch**v2

```XML
<launch>
  <node pkg="hello_ros" type="talker_node" name="talker" output="screen">
    <param name="rate" value="5" />
  </node>

  <node pkg="hello_ros" type="listener_node" name="listener" output="screen" />
```

### **13\.3 重新编译并运行**

bash

`cd ~/catkin_ws catkin_make roslaunch hello_ros start.launch`

---

## **VS Code 中的“好用设置”（让补全/跳转更丝滑）**

### **14\.1 关键原则：确保 VS Code 继承 ROS 环境**

最推荐的方式仍然是：

bash

`cd ~/catkin_ws code .`

### **14\.2 C/C\+\+ IntelliSense 找不到 ros/ros\.h 怎么办？**

常见原因是 includePath 未配置或环境未继承。按顺序排查：

1. 确认已安装 `ros-noetic-roscpp`

2. 确认你是从“已 source 环境的终端”打开 VS Code

3. 重新编译一次 `catkin_make`

4. VS Code 命令面板（Ctrl\+Shift\+P）里执行： 

    - `C/C++: Reset IntelliSense Database`

> 进阶做法：生成 compile\_commands\.json 给 clangd/IntelliSense（后续你需要我可以再写一节“最佳实践配置”）。
> 
> 

---

## **Copilot 在 ROS 学习中的正确用法（建议）**

Copilot 很适合做：

- 生成节点模板（publisher/subscriber/service）

- 快速补全 CMakeLists

- 根据你描述生成 launch 文件骨架

- 写注释、日志、参数读取、简单类封装

但你仍应自己掌握：

- Topic 名称与消息类型

- roscore/roslaunch/rosrun 的区别

- 工作空间结构与 catkin 编译流程

建议你在代码里先写“意图注释”，再让 Copilot 补全，例如：

`// TODO: create a publisher to /cmd_vel at 20Hz and publish geometry_msgs::Twist`

---

# **附：ROS 入门“最小知识地图”**

1. **节点（node）**：一个运行中的进程（你的 executable）

2. **话题（topic）**：发布/订阅的消息通道（异步）

3. **消息（msg）**：通信数据结构（如 std\_msgs/String）

4. **参数（param）**：运行时配置（可通过 launch/命令行设置）

5. **launch**：一键启动多个节点 \+ 参数 \+ 重映射

6. **工作空间（catkin\_ws）**：你的所有包的集合

7. **catkin\_make**：构建整个工作空间

