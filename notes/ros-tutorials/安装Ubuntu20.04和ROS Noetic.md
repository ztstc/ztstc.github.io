# 安装Ubuntu20\.04和ROS Noetic

> 目标读者：第一次安装 Ubuntu/ROS 的同学；希望快速把 ROS Noetic 跑起来并能创建工作空间、跑小乌龟/rviz 的同学。
> 
> 推荐环境：**Ubuntu 20\.04 LTS（Focal）\+ ROS Noetic**（Noetic 官方主要面向 20\.04）。
> 
> 安装方式覆盖：
> 
> 1. **Windows 双系统（推荐）**
> 
> 2. **VMware/VirtualBox 虚拟机（不推荐，仅用于尝鲜 容易卡顿）**
> 
> 3. **macOS 虚拟机（UTM/Parallels/VMware Fusion）**
> 
> 

---

## 安装前的准备（重要）

### 0\.1 硬件建议

- CPU：4 核及以上更舒适（ROS \+ 编译 \+ rviz 更吃 CPU）

- 内存：**16GB 推荐**（至少 8GB）

- 磁盘：Ubuntu 分区或虚拟磁盘建议 **\>= 128GB**（含 ROS、依赖、工程、bag 等）

- 显卡：有独显更好；虚拟机里 3D 加速往往不稳定，是“不推荐虚拟机”的原因之一

### 0\.2 下载清单

- Ubuntu 20\.04 LTS ISO（Desktop 版）

- 制作启动盘工具（Windows）：Rufus / balenaEtcher / Ventoy

- （可选）驱动：NVIDIA 驱动在装完 Ubuntu 后再装

### 0\.3 网络与源

- ROS/apt 包下载依赖网络质量。建议： 

    - 先保证能稳定访问外网/镜像源

    - 之后再进行 rosdep 初始化与依赖安装

    - 连接杭电教学区网络或者准备梯子

---

## Windows 双系统安装 Ubuntu 20\.04（推荐）

> 这是最接近真实开发/部署环境的方式：对硬件访问更直接，USB/串口/LiDAR/相机等外设支持最佳。
> 
> 

### 1\.1 Windows 侧准备

1. **备份数据**：重要文件先备份（任何分区操作都有风险）

2. **关闭快速启动**（可显著减少双系统时钟/挂载问题） 

    - 控制面板 → 电源选项 → 选择电源按钮的功能 → 更改当前不可用设置 → 取消勾选“启用快速启动”

3. **为 Ubuntu 腾出空间（推荐 128GB\+）**

    - 右键“此电脑”→ 管理 → 磁盘管理

    - 选择空间富余的分区 → 压缩卷 → 留出未分配空间（不要新建卷）

### 1\.2 制作 Ubuntu 启动 U 盘

1. 插入 U 盘（建议 8GB\+）

2. 用 Rufus / balenaEtcher / Ventoy 写入 Ubuntu 20\.04 ISO 

    - 常见选择： 

        - 分区类型：GPT（较新电脑 UEFI 一般用 GPT）

        - 目标系统：UEFI（非 CSM）

3. 写入完成后安全弹出

### 1\.3 BIOS/UEFI 设置（不同机型略有差异）

- 进入 BIOS（常见：F2/F10/Del/Esc）

- 建议： 

    - **（重要）关闭 Secure Boot**（有时会影响第三方驱动/引导）

    - 启用 UEFI 启动

    - 调整启动顺序：U 盘优先

### 1\.4 安装 Ubuntu（关键步骤）

1. 从 U 盘启动，选择  “Install Ubuntu”

2. 语言/键盘布局按习惯选择

3. 更新与软件： 

    - 建议选择 **Normal installation**

    - 勾选 “Install third\-party software …”（可装常见驱动/解码器）

4. **安装类型（重点）**

    - 推荐选择：**Install Ubuntu alongside Windows Boot Manager**

    - 如果没有该选项，选择 “Something else” 手动分区： 

        - 在“未分配空间”上创建： 

            - `/` 根分区：ext4，**40GB\+**

            - `swap`：一般 8GB～16GB（内存 16GB 可设 8GB；需要休眠则 swap \>= 内存）

            - `/home`：ext4，其余空间（可选，但推荐）

        - 引导器安装位置：通常选择系统盘的 EFI 分区所在磁盘（如 `/dev/nvme0n1`）

5. 安装完成后重启，拔掉 U 盘

6. 启动时会出现 GRUB 菜单，选择 Ubuntu 或 Windows

### 1\.5 双系统常见问题

- **时间不一致**（Windows 与 Ubuntu 时间差 8 小时）：

```Bash
timedatectl set-local-rtc 1 --adjust-system-clock
```

- **Windows 分区只读/无法挂载**：多半是 Windows 快速启动没关或休眠文件导致

    - 确认 Windows 关机不是“休眠/快速启动关机”，并关闭快速启动

- **NVIDIA 驱动**：

    - Ubuntu 里：Software \& Updates → Additional Drivers → 选择推荐驱动 → Apply

    - 重启后再用 `nvidia-smi` 验证

---

## VMware/VirtualBox 虚拟机安装 Ubuntu 20\.04（不推荐）

> 不推荐原因：图形/3D 加速、USB 设备透传、相机/LiDAR/串口延迟等问题常见；跑 rviz、gazebo 体验差。
> 
> 适合：只想快速体验命令行、学基础 ROS 概念、不接硬件的场景。
> 
> 

### 2\.1 虚拟机配置建议

- CPU：4 核（至少 2 核）

- 内存：8GB（至少 4GB）

- 磁盘：60GB 动态分配

- 显示：开启 3D 加速（但可能不稳定）

- 网络：NAT（简单）或桥接（需要局域网互通时）

### 2\.2 安装流程

- 挂载 Ubuntu ISO → 按安装向导安装（与真机类似）

- 装完后建议安装增强工具： 

    - VMware Tools / VirtualBox Guest Additions（改善分辨率、剪贴板、文件拖拽等）

---

## macOS 上安装 Ubuntu 虚拟机（UTM/Parallels/Fusion）

### 3\.1 Apple Silicon（M1/M2/M3）特别说明

- **需要使用 ARM 架构 Ubuntu（aarch64）** 的镜像（不要用 x86\_64 的 ISO）

- ROS Noetic 官方主要面向 Ubuntu 20\.04 **x86\_64** 生态更成熟；在 ARM 上可能遇到包缺失/编译问题

- 如果你是 Apple Silicon，且目标是 ROS1（Noetic），建议优先考虑： 

    - 远程连接一台 x86 Ubuntu 机器（本地用 VSCode Remote / SSH）

    - 或直接上 ROS2（但这与 Noetic 不是同一条线）

### 3\.2 Intel Mac

- 用 Parallels / VMware Fusion 装 x86 Ubuntu 20\.04 较顺滑

- 依然存在虚拟机对外设、实时性、3D 的限制

---

# 二、Ubuntu 20\.04 基础配置（装完必做）

## 0\.设置密码

- 密码尽量设置简单点 以后sudo、钥匙链都需要密码 例如“1““123456”

## 更新系统与常用工具

```Bash
sudo apt update
sudo apt -y upgrade
sudo apt -y install curl wget git vim net-tools build-essential
```

## 设置时区与时间同步（可选但推荐）

```Bash
sudo timedatectl set-timezone Asia/Shanghai
sudo apt -y install chrony
sudo systemctl enable --now chrony
```

## 配置 Git（建议）

```Bash
git config --global user.name "yourname"
git config --global user.email "you@example.com
```

---

# 三、安装 ROS Noetic（强烈推荐：鱼香ROS 一键安装）

> 鱼香ROS（小鱼）的一键脚本能自动处理源、依赖、rosdep 等步骤，适合新手快速完成 ROS 安装。
> 
> 下面给出通用操作流程；脚本菜单中通常可以选择 ROS1/ROS2、版本、桌面版等。
> 
> 小鱼的官网：[https://fishros\.org\.cn/forum/topic/20/小鱼的一键安装系列](https://fishros.org.cn/forum/topic/20/%E5%B0%8F%E9%B1%BC%E7%9A%84%E4%B8%80%E9%94%AE%E5%AE%89%E8%A3%85%E7%B3%BB%E5%88%97)
> 
> 

## 一键安装 ROS Noetic（推荐路线）

1. 打开终端，先确保网络正常（能 `ping` 通外网或镜像源）

2. 运行一键安装脚本（按提示选择 ROS Noetic）

```Bash
# 说明：不同时间脚本入口可能更新，请以鱼香ROS官方说明为准
wget <http://fishros.com/install> -O fishros && . fishros
```

1. 脚本执行过程中你一般会选择：

    - 安装 ROS1 → Noetic

    - 选择 `desktop-full`（新手推荐，带 rviz、rqt 等常用工具）

## 安装完成后的环境生效

安装完成后通常会提示你将 ROS 环境写入 `~/.bashrc`。你也可以手动确认：

```Bash
# 检查 ~/.bashrc 里是否有类似这行
# source /opt/ros/noetic/setup.bash

source ~/.bashrc
```

## 验证 ROS 是否安装成功

```Bash
rosversion -d          # 应输出 noetic
printenv | grep ROS
```

---

# 四、初始化 rosdep（非常关键）

> rosdep 用于自动安装 ROS 包依赖。很多编译失败/缺依赖都和它相关。
> 
> 

```Bash
sudo rosdep init
rosdep update
```

若 `rosdep update` 慢或失败，多半是网络或源问题；建议确认 DNS/代理/镜像配置。

---

# 五、创建 catkin 工作空间并编译（ROS1标准流程）

```Bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
```

编译成功后，加载工作空间环境（建议写入 `.bashrc`）：

```Bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

# 六、运行经典例子验证（小乌龟 \+ rqt\_graph）

> 需要至少两个终端窗口（都要先 source \~/\.bashrc，一般自动生效）
> 
> 

### 6\.1 启动 roscore（终端 1）

```Bash
roscore
```

### 6\.2 启动小乌龟（终端 2）

```Bash
rosrun turtlesim turtlesim_node
```

### 6\.3 键盘控制（终端 3）

```Bash
rosrun turtlesim turtle_teleop_key
```

### 6\.4 查看计算图（终端 4，可选）

```Bash
rqt_graph
```

---

# 七、常见问题排查

## 1\) `command not found: roscore/rosrun`

- 没有 source ROS 环境：

```Bash
source /opt/ros/noetic/setup.bash
```

- 或 `.bashrc` 没生效：重新打开终端或 `source ~/.bashrc`

## rosdep 初始化失败

- 检查网络/DNS

- 确认 `sudo rosdep init` 已执行且无报错

- 重试：

```Bash
rosdep update
```

## 虚拟机 rviz/gazebo 很卡或打不开

- 尝试开启 3D 加速、提高显存

- 仍不行：建议换双系统/真机 Ubuntu

## 需要串口权限（USB 转串口/IMU/GNSS 常用）

```Bash
sudo usermod -a -G dialout $USER
# 重新登录或重启后生效
```

---

# 八、推荐安装的常用 ROS 工具包（可选）

```Bash
sudo apt -y install \\\\
  python3-rosdep \\\\
  python3-catkin-tools \\\\
  ros-noetic-rqt \\\\
  ros-noetic-rqt-common-plugins \\\\
  ros-noetic-tf2-tools \\\\
  ros-noetic-teleop-twist-keyboard
```

---

对于常见的办公软件 如Chrome VScode QQ 微信 WPS 都是有Ubuntu版本的 可以自行去官网搜索下载

**注意 绝对不要在Snap应用商店下载任何软件！**

# 九、常见故障

- 画面卡顿 显示器以最大亮度工作

    - 显卡驱动未安装 尝试手动安装

- wifi蓝牙无法连接 搜索不到设备

    - 对于新电脑而言 Wifi7网卡没有系统支持 可能需要淘宝买个免驱动的无线网卡19\.9元一个

    - 蓝牙和wifi是一体的 所以也会这样

- 触摸板不工作

- 中文输入法故障

- 字太小了 想要放大 打开分数比例缩放 尝试更改



