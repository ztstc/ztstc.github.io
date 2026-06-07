# 2025.2版本Vivado Xilinx7020入门学习笔记 Vitis 点灯 汉化 

## 概要

7020属于特殊的FPGA，它将ARM A9双核和现场可编程门电路阵列即PS（Processing System)和PL(Programmable Logic)通过AXI总线进行连接和通信

因为这种胶水双架构的特殊性，开发这两种架构需要不同的编辑器

下面的笔记使用**2025.2版本**的编辑器，页面选择**新版IDE**（有点太新了，没啥资料，bug还多司马了）

PS ARM开发类似STM32 我们使用C开发 软件是Vitis类似VScode可装Cline等插件**(有bug)**

[跳转本文：Vitis插件重启后消失](#bug1)

PL FPGA开发比较特殊 使用Verilog进行开发 软件是Vivado

​	有关软件下载：https://china.xilinx.com/support/download/index.html/content/xilinx/zh/downloadNav/vivado-design-tools.html

​	有关Verilog语法：http://www.hellofpga.com/index.php/2023/04/06/verilog_01/

Vitis可以在Vivado的tool栏中启动

**XDC** 是 **Xilinx Design Constraints** 的缩写，即 **赛灵思设计约束文件**。

它是 Vivado 开发套件中用于定义 **FPGA 设计物理与时序规则** 的标准文件格式（基于 Tcl 脚本语言）。

核心作用

1. **引脚约束**：将设计中的逻辑端口映射到芯片的物理引脚，并指定电平标准（如 LVCMOS33）。
2. **时序约束**：定义时钟频率、输入输出延迟等，确保设计能在预期速度下稳定工作（如 `create_clock`、`set_input_delay`）。
3. **布局布线指导**：例如告诉工具哪些逻辑应该放在特定区域（`pblock`），或者哪些路径可以放松要求（`set_false_path`）。

## 启动软件

如果安装没问题的话，终端直接输入 回车就可以了

启动Vivado

```bash
vivado
```

启动Vitis

```bash
vitis
```

## UI切换

下文的Vivado页面都是基于新版页面截图

在顶部栏找到Tools - Settings

打开New Vivado IDE即可

![image-20260517164249220](assets/image-20260517164249220.png)

## 中文页面切换

### Vivado

Vivado基本没有做汉化

在顶部栏找到Tools - Settings

<img src="assets/image-20260517122410491.png" alt="image-20260517122410491" style="zoom: 33%;" />

Help - Language 选简体中文Chinese Simplified

<img src="assets/image-20260517122344315.png" alt="image-20260517122344315" style="zoom: 33%;" />

切换了发现页面依然是英文 但是将鼠标放在某个选项上时**窗口左下角**有时会出现中文提示(疑似机翻)

### Vitis

Vitis由于是套壳VScode 所以可以在插件栏安装VScode版本的简体中文插件

<img src="assets/image-20260517144205555.png" alt="image-20260517144205555" style="zoom:33%;" />

安装时会提示未经过验证 无视风险继续安装

安装完成之后不会自动切换语言

需要Ctrl + Shift + P 输入 **Configure Display Language** 

选择中文

<img src="assets/image-20260517144712623.png" alt="image-20260517144712623" style="zoom:33%;" />

然后重启

<img src="assets/image-20260517144522729.png" alt="image-20260517144522729" style="zoom:50%;" />

部分经过Vitis修改的内容是没有汉化的，插件的兼容性问题有待观察

**有bug**

[跳转本文：Vitis插件重启后消失](#bug1)

## Helloworld点灯

**简介**

参考教程（由于版本差异请不要遵循 这个是2018版的）：

http://www.hellofpga.com/index.php/2023/11/04/vitis/

### **一、 硬件介绍**

为了演示两个按键的功能，这里再引入两个指示灯，将LED的驱动脚拉高，指示灯亮，拉低指示灯熄灭，指示灯分别接在主芯片的P20和P21脚

<img src="http://www.hellofpga.com/wp-content/uploads/2023/04/image-21.png" alt="img" style="zoom:33%;" />

### **二、创建Vivado工程**

1.启动Vivado

2.创建新项目

<img src="assets/image-20260517172336935.png" alt="image-20260517172336935" style="zoom:33%;" />

3.命名项目 -Next

<img src="assets/image-20260517172557778.png" alt="image-20260517172557778" style="zoom: 25%;" />



4.选择RTL Project  -Next

<img src="assets/image-20260517172753444.png" alt="image-20260517172753444" style="zoom:25%;" />

5.留空  -Next

<img src="assets/image-20260517172944928.png" alt="image-20260517172944928" style="zoom:25%;" />

6.留空  -Next

<img src="assets/image-20260517173112847.png" alt="image-20260517173112847" style="zoom:25%;" />

7.选择芯片型号 **（xc7z020clg484-1）**

<img src="assets/image-20260517173201886.png" alt="image-20260517173201886" style="zoom:25%;" />

8.Finish

<img src="assets/image-20260517173251104.png" alt="image-20260517173251104" style="zoom:25%;" />

### **三、 创建一个BLOCK设计**

9.IP INTEGRATOR→Create Block Design，在弹出的对话框中输入设计名，最后点击“OK”，如下图所示

<img src="assets/image-20260517173506046.png" alt="image-20260517173506046" style="zoom:33%;" />

10.在右侧的窗口里 ，点击加号，在选择框里搜索ZYNQ，并找到ZYNQ7 PROCESSING SYSTEM ，双击并打开

<img src="assets/image-20260517173610574.png" alt="image-20260517173610574" style="zoom: 33%;" />

11.软件自动生成了一个 zynq的block 如下图所示，接下来要做一些相应的设置，双击下图中的ZYNQ核

<img src="assets/image-20260517173730783.png" alt="image-20260517173730783" style="zoom:33%;" />

12.依次在弹窗里找到DDR Configuration→DDR Controller Configuration→DDR3，在Memory Part下拉菜单中根据自己板子上的DDR来选择相应的DDR3，本实验所用到型号：MT41K256M16RE-125**(这个看你的开发板资料）**，数据位宽选择16bit **(这个看你的开发板资料）**最后点击“OK”,如下图所示。

<img src="assets/image-20260517174701174.png" alt="image-20260517174701174" style="zoom: 33%;" />

13.在PS的MIO配置选项的GPIO栏里，**勾选GPIO**，增加两路EMIO（因为本次测试的是两个，如果需要增加按键或者其它IO 这里可以对应的调整）

<img src="assets/image-20260517174803796.png" alt="image-20260517174803796" style="zoom:33%;" />

14.OK退出，然后点击“Run Block Automation”如下图所示。在弹出的选项中保持默认，点击“OK”，即可完成对ZYNQ7 Processing System的配置

<img src="assets/image-20260517174856571.png" alt="image-20260517174856571" style="zoom:33%;" />

<img src="assets/image-20260517175007311.png" alt="image-20260517175007311" style="zoom: 25%;" />

15.将刚才添加EMIO GPIO 引出 右键GPIO_0—->Make External

<img src="assets/image-20260517175036390.png" alt="image-20260517175036390" style="zoom:33%;" />

如图

<img src="assets/image-20260517175149205.png" alt="image-20260517175149205" style="zoom:33%;" />

16.鼠标按住拖动线，用线将M_AXI_GP0_ACLK与 FCLK_CLK0连接起来 **(也可以在配置页面禁用AXI 就不需要连接了)**鼠标放开就能自动连线

<img src="assets/image-20260517175743991.png" alt="image-20260517175743991" style="zoom: 50%;" />

<img src="assets/image-20260517175818258.png" alt="image-20260517175818258" style="zoom: 50%;" />

17.source→Design Source ，右键我们创建的BLOCK工程，点击create HDL wrapper如下图所示。

<img src="assets/image-20260517185734887.png" alt="image-20260517185734887" style="zoom:33%;" />

在弹出的对话框里保持默认

<img src="assets/image-20260517185818663.png" alt="image-20260517185818663" style="zoom:33%;" />

软件自动为我们生成HDL文件

<img src="assets/image-20260517185844074.png" alt="image-20260517185844074" style="zoom:33%;" />

### **四、创建约束文件，并且定义管脚**

（这里使用约束方式，也可以在RTL配置界面手动选择管脚）

1）Add Source → Add or create constraints 点Next

<img src="assets/image-20260517190127781.png" alt="image-20260517190127781" style="zoom: 25%;" />

因为这个项目没有创建过约束文件 所以这里创建`Create File`一个约束文件，并在File name 里设置约束文件的名称LED_TEST，并且点击FINISH 完成约束文件的创建

<img src="assets/image-20260517190250298.png" alt="image-20260517190250298" style="zoom:25%;" />

<img src="assets/image-20260517190313510.png" alt="image-20260517190313510" style="zoom:25%;" />

2）Sources → Constraints 里找到刚才创建的约束文件 双击并打开该XDC约束文件

<img src="assets/image-20260517190441961.png" alt="image-20260517190441961" style="zoom: 33%;" />

在约束文件里面复制下面代码来对输出的GPIO进行设置（所有的管脚转接板上丝印都有实际标注对应的IO）

[跳转本文：XDC代码解释](#code2)

```tcl
set_property IOSTANDARD LVCMOS33 [get_ports GPIO_0_0_tri_io[0]]
set_property IOSTANDARD LVCMOS33 [get_ports GPIO_0_0_tri_io[1]]

set_property PACKAGE_PIN P20 [get_ports GPIO_0_0_tri_io[0]]
set_property PACKAGE_PIN P21 [get_ports GPIO_0_0_tri_io[1]]
```

<img src="assets/image-20260517190632380.png" alt="image-20260517190632380" style="zoom:50%;" />

### **五、生成bit文件**

按下绿色箭头对工程进行编译 

**Run Synthesis**（运行综合）和 **Run Implementation**（运行实现） 需要先后执行

![image-20260517190707681](assets/image-20260517190707681.png)

在弹出的窗口选Save

<img src="assets/image-20260517190940701.png" alt="image-20260517190940701" style="zoom: 50%;" />

等待右上角圈圈转完

<img src="assets/image-20260517191103165.png" alt="image-20260517191103165" style="zoom: 50%;" />

转完之后会弹窗

<img src="assets/image-20260517191139227.png" alt="image-20260517191139227" style="zoom:50%;" />

此时选择OK就会开始**Run Implementation**（运行实现） 后面就不需要另外点了

等待右上角圈圈转完

<img src="assets/image-20260517191231245.png" alt="image-20260517191231245" style="zoom:50%;" />

生成结束后会弹窗

<img src="assets/image-20260517191314030.png" alt="image-20260517191314030" style="zoom:50%;" />

选择Generate Bitstream则不需要另外点击![image-20260517191349838](assets/image-20260517191349838.png)这个按钮了

等待右上角圈圈转完

<img src="assets/image-20260517191431403.png" alt="image-20260517191431403" style="zoom:50%;" />

到这一部就结束了

<img src="assets/image-20260517191514030.png" alt="image-20260517191514030" style="zoom:50%;" />

点叉叉退出

### **六、vitis 工程创建**

**1）导出硬件**

File→Export→Export hardware…

<img src="assets/image-20260517191639176.png" alt="image-20260517191639176" style="zoom:50%;" />

勾选 **include bitstream** ，再选择Next

<img src="assets/image-20260517191902737.png" alt="image-20260517191902737" style="zoom: 33%;" />

记录下导出的地址，然后选择Next

<img src="assets/image-20260517192045545.png" alt="image-20260517192045545" style="zoom: 33%;" />

之后选择Finish

<img src="assets/image-20260517192115380.png" alt="image-20260517192115380" style="zoom:33%;" />

**2 ）启动vitis，并创建工程**

1）在vivado中启动：Tools -> launch vitis IDE或者在终端输入`vitis`

<img src="assets/image-20260517192830076.png" alt="image-20260517192830076" style="zoom:33%;" />

<img src="assets/image-20260517192853973.png" alt="image-20260517192853973" style="zoom:33%;" />

2） 启动 vitis 后，将workspace 定义在工程目录下 **（备注目录名称不能带中文）**

<img src="assets/image-20260517193003435.png" alt="image-20260517193003435" style="zoom:33%;" />

<img src="assets/image-20260517193050299.png" alt="image-20260517193050299" style="zoom: 25%;" />

<img src="assets/image-20260517193158595.png" alt="image-20260517193158595" style="zoom: 33%;" />

点更新

3） 点选New Component Platform 创建工程

<img src="assets/image-20260517193331752.png" alt="image-20260517193331752" style="zoom:33%;" />

为platform命名 - 点选Next

<img src="assets/image-20260517193411083.png" alt="image-20260517193411083" style="zoom:33%;" />



4） 选择Hardware Design 点击Browse

从现有的xsa文件创建工程 ，并按下图所示，找到并加载我们的xsa文件

<img src="assets/image-20260517193508261.png" alt="image-20260517193508261" style="zoom:33%;" />

<img src="assets/image-20260517193645548.png" alt="image-20260517193645548" style="zoom:33%;" />

选中后点击Next

<img src="assets/image-20260517193713166.png" alt="image-20260517193713166" style="zoom:33%;" />

保持默认 - 点击Next

standalone是裸机的意思 （其他的选项有freertos和linux，但是这次不用）

<img src="assets/image-20260517193736682.png" alt="image-20260517193736682" style="zoom:33%;" />

完成 Finish

<img src="assets/image-20260517194012224.png" alt="image-20260517194012224" style="zoom:33%;" />

等待加载完毕之后 左上角会出现platform

<img src="assets/image-20260517194106092.png" alt="image-20260517194106092" style="zoom:50%;" />

7） 选择创建一个空工程应用 点选New Component Application 创建工程应用

<img src="assets/image-20260517194131407.png" alt="image-20260517194131407" style="zoom: 50%;" />

为工程应用命名LED_TEST - 点选Next

<img src="assets/image-20260517194307596.png" alt="image-20260517194307596" style="zoom: 33%;" />

点击选中高亮我们刚才创建的platform - Next

<img src="assets/image-20260517194414517.png" alt="image-20260517194414517" style="zoom:33%;" />

Next

<img src="assets/image-20260517194455552.png" alt="image-20260517194455552" style="zoom:33%;" />

留空 - Next

<img src="assets/image-20260517194508849.png" alt="image-20260517194508849" style="zoom:33%;" />

Finish完成

<img src="assets/image-20260517194545198.png" alt="image-20260517194545198" style="zoom:33%;" />

项目创建完成后注意到左上角出现工程应用

<img src="assets/image-20260517194629010.png" alt="image-20260517194629010" style="zoom: 50%;" />

展开LED_TEST工程应用

依次展开Sources  - src

<img src="assets/image-20260517194656641.png" alt="image-20260517194656641" style="zoom:50%;" />

右键src创建新文件New File

<img src="assets/image-20260517194815046.png" alt="image-20260517194815046" style="zoom:50%;" />

新文件叫`main.c `  - 确定

<img src="assets/image-20260517194852362.png" alt="image-20260517194852362" style="zoom:50%;" />

打开刚才创建的main.c 然后 写入以下代码

有一个地方值得注意 EMIO的 IO口编号 是从54开始的，也就是我VIVADO 下创建的 EMIO端口，在PS端都是从54-55-56 依次排序的（小贴士 小于54的是MIO 也就是芯片PS的硬件IO口）

[跳转本文：main.c代码解释](#code1)

```c
#include "xparameters.h"
#include "xgpiops.h"
#include "xstatus.h"
#include "xplatform_info.h"
#include "sleep.h"

#define LED1    	54
#define LED2  		55

#define GPIO_DEVICE_ID  	0
XGpioPs Gpio;


void Gpio_Init(void){
	XGpioPs_Config *ConfigPtr;

	ConfigPtr = XGpioPs_LookupConfig(GPIO_DEVICE_ID);
	XGpioPs_CfgInitialize(&Gpio, ConfigPtr,ConfigPtr->BaseAddr);

	XGpioPs_SetDirectionPin(&Gpio, LED1, 1);
	XGpioPs_SetOutputEnablePin(&Gpio, LED1, 1);

	XGpioPs_SetDirectionPin(&Gpio, LED2, 1);
	XGpioPs_SetOutputEnablePin(&Gpio, LED2, 1);

	XGpioPs_WritePin(&Gpio, LED1, 0);
	XGpioPs_WritePin(&Gpio, LED2, 0);
}



int main(void)
{
	Gpio_Init();

	while(1){

		XGpioPs_WritePin(&Gpio, LED1, 0);
		XGpioPs_WritePin(&Gpio, LED2, 0);

		sleep(1);

		XGpioPs_WritePin(&Gpio, LED1, 1);
		XGpioPs_WritePin(&Gpio, LED2, 1);

		sleep(1);

	};

	return 0;
}
```

注意新版代码和之前有所不同

```c
#define GPIO_DEVICE_ID  	0  //新
#define GPIO_DEVICE_ID  	XPAR_XGPIOPS_0_DEVICE_ID // 老
```

深呼吸 爆红是正常的

<img src="assets/image-20260517195217153.png" alt="image-20260517195217153" style="zoom:33%;" />

点击左下角 Build

<img src="assets/image-20260517195443003.png" alt="image-20260517195443003" style="zoom:50%;" />

点Alaways build platform with application(全部重新编译) 

和Save in Workspace Preference比较保险（相对费时）

<img src="assets/image-20260517195250129.png" alt="image-20260517195250129" style="zoom:33%;" />

只要提示Build successfully ,左下角RUN绿色勾 就说明成功！

<img src="assets/image-20260517195331230.png" alt="image-20260517195331230" style="zoom:33%;" />

点击左下角Run

<img src="assets/image-20260517195834468.png" alt="image-20260517195834468" style="zoom:50%;" />

注意到FPGA的板载LED同时开始闪烁

如果报错说没有连接，则查看[跳转本文：找不到设备](#bug2)

## 问题记录

<a id="bug1"> 我已急哭</a>

### Bug： Vitis 每次重启后插件都消失（已验证）

每次重启 Vitis 后插件都消失，这是 Vitis IDE（特别是 2025.1 和 2025.2 版本）一个已知的 bug，主要和它的“在线安装”功能有关。

具体来说，通过 IDE 内置市场在线安装的插件，会被存放在一个 IDE 重启后无法正确识别的路径下，造成了“消失”的假象。

解决方案：

**手动转移插件目录**

1.  **关闭**正在运行的 Vitis IDE。
2.  打开文件管理器，进入插件存储目录 `~/.Xilinx/Vitis/2025.2/.vitis/`（请将 `2025.2` 替换为你的具体版本号）。
3.  在这个目录下，你会找到两个文件夹：`extensions/` 和 `deployedPlugins/`（如果没有就在`~/.Xilinx/Vitis/2025.2/.vitis/`目录内自己创建一个`mkdir -p deployedPlugins`）。
    *   `extensions/`：存放通过“在线安装”的插件。
    *   `deployedPlugins/`：存放通过“离线安装”的插件。
4.  将 `extensions/` 文件夹里的**所有内容**，**剪切并粘贴**到 `deployedPlugins/` 文件夹里。
5.  **重新启动** Vitis IDE，消失的插件应该就会重新出现了。

### Bug： Vitis 启动后终端报错

![image-20260517155918663](assets/image-20260517155918663.png)

这个错误是典型的 **Python 环境冲突** 导致的，根本原因是：

> ROS 2 的 Python 脚本启动时，意外加载了 **Vivado 2025.2 自带的 Python 库**（路径 `/home/zhengtuo/Vivado/2025.2/Vivado/tps/lnx64/python-3.13.0/`），而这个 Vivado 的 Python 环境与系统的 `_sre`（正则表达式底层C模块）不兼容，导致 `SRE module mismatch` 断言失败。

**为什么会发生？**

- 你的系统里安装了 **ROS 2 Jazzy**（使用系统默认 Python，通常是 3.10 或 3.12）。
- 你也安装了 **Vivado 2025.2**，它自带了一个独立的 Python 3.13 环境。
- 你的终端环境变量（比如 `PATH`、`PYTHONPATH` 或 `LD_LIBRARY_PATH`）中，**Vivado 的 Python 路径被排在了系统 Python 路径之前**。
- 当 ROS 2 的 `_local_setup_util.py` 脚本运行时，它试图导入 `argparse`，进而导入 `re` 模块，结果却找到了 Vivado 提供的 `re.py` 和对应的 `_sre.so` C 扩展。
- Vivado 的 `_sre.so` 是为其自带的 Python 3.13 编译的，但当前运行的 Python 解释器可能是系统的（3.10/3.11/3.12），两者魔数不匹配，于是报错。

**解决方法**

**方案一：临时修复（单次运行 ROS 2 前清理环境）**

在终端中，运行任何 ROS 2 命令之前，先执行以下命令，临时移除 Vivado 的 Python 路径：

```bash
# 删除 Vivado 添加的 Python 路径（注意这个路径可能通过多种环境变量注入）
export PATH=$(echo $PATH | tr ':' '\n' | grep -v '/home/zhengtuo/Vivado/2025.2' | tr '\n' ':')
export PYTHONPATH=$(echo $PYTHONPATH | tr ':' '\n' | grep -v '/home/zhengtuo/Vivado/2025.2' | tr '\n' ':')
export LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH | tr ':' '\n' | grep -v '/home/zhengtuo/Vivado/2025.2' | tr '\n' ':')
```

然后重新 source ROS 2 环境：
```bash
source /opt/ros/jazzy/setup.bash
```

现在再运行 ROS 2 命令应该就正常了。

**方案二：永久修复（调整 Vivado 环境变量的加载时机）**

如果你平时 **不同时使用 ROS 2 和 Vivado**，可以将 Vivado 的环境变量脚本移动到**按需加载**，而不是每次都自动添加到 `~/.bashrc` 中。

1. 打开 `~/.bashrc`，找到类似这样的行：
   ```bash
   source /home/zhengtuo/Vivado/2025.2/settings64.sh
   ```
2. 把它注释掉（行首加 `#`），然后改为一个函数别名：
   ```bash
   alias vivado_setup='source /home/zhengtuo/Vivado/2025.2/settings64.sh'
   ```
3. 保存后执行 `source ~/.bashrc`。

之后，你需要使用 Vivado 时，先执行 `vivado_setup` 再运行 `vivado`；平时做 ROS 2 开发时不会加载 Vivado 的环境，冲突就不会发生。

**方案三：彻底隔离（使用虚拟环境或容器）**

- 为 ROS 2 和 Vivado 分别建立**不同的终端会话**，或者使用 `conda` / `venv` 管理 Python 环境，避免路径交叉。
- 更彻底的方式：用 Docker 容器跑 Vivado 或 ROS 2，物理上隔离环境。

**验证是否解决**

运行以下命令，检查当前 Python 的 `sys.path` 中是否还有 Vivado 路径：

```bash
python3 -c "import sys; print('\n'.join(sys.path))" | grep Vivado
```

如果没有任何输出，说明环境已干净。再运行 ROS 2 命令（如 `ros2 --help`）应该就不会报错了。

如果以上方法仍无法解决，请提供你 `~/.bashrc` 中与 Vivado、ROS 2 相关的行，我可以帮你进一步分析。

<a id="bug2"> </a>

### Bug： Vitis 和 Vivado都找不到设备（已解决）

如果在Vitis RUN报错

Could not find ARM device on the board for connection 'Local'. Check if the target is in: 1. Split JTAG - No operations are possible with ARM DAP. 2. Non JTAG bootmode - Bootrom may need time to enable DAP. Please try again. Troubleshooting hints: 1. Check whether board is connected to system properly. 2. In case of zynq board, check whether Digilent/Xilinx cable switch settings are correct. 3. If you are using Xilinx Platform Cable USB, ensure that status LED is green.

安装下驱动

```
# 进入 Vitis/Vivado 安装目录下的脚本位置（根据你的实际路径修改）
cd /tools/Xilinx/Vivado/2025.2/data/xicom/cable_drivers/lin64/install_script/install_drivers/
# 运行安装脚本（需要 sudo）
sudo ./install_drivers
```



那么看看lsusb有没有链接上

![image-20260517170250065](assets/image-20260517170250065.png)

没问题 说明硬件是好的

检查 Zynq 启动模式跳线

- **JTAG 模式**：跳线设为 `0000`（全部接地）。
- 如果设为 SD/QSPI/NAND 等非 JTAG 模式，上电后 Zynq 会直接执行外部存储器代码，不会响应 JTAG 扫描，导致找不到 ARM DAP。

在 Vitis / Vivado Hardware Manager 中扫描设备 出现芯片就没问题了

![image-20260517170055851](assets/image-20260517170055851.png)

### 问题：RUN了之后为啥断电重启程序就没了

原因：RUN的本质是将程序放在内存当中运行，断电当然消失

如果要把程序持久化运行 可以把程序放在FLASH里面上电自动运行

标准的固化流程分为两步：

1**烧录阶段：使用 JTAG 模式**

- 板子启动跳线设为 **JTAG 模式**。
- 在 Vitis 中通过 JTAG 将 `BOOT.bin` **烧写到 QSPI Flash** 芯片中（相当于把程序“刻录”进非易失存储器）。
- 此时 Flash 里有了数据，但板子还在 JTAG 模式下，上电后仍等待 JTAG 命令，不会自动执行 Flash 里的程序。

2 **运行阶段：切换到 QSPI 模式**

- **断电**板子，将启动跳线改为 **QSPI Boot 模式**。
- **重新上电**，Zynq 的 BootROM 就会自动从 QSPI Flash 读取 `BOOT.bin`，加载并运行你的程序。

为什么不能在 QSPI 模式下直接烧录？

在 QSPI 模式下，芯片上电后会立即**从 Flash 中执行代码**，此时 Flash 被控制器占用。如果此时尝试通过 JTAG 往同一个 Flash 写入数据，就会发生**总线冲突**，导致烧录失败或系统崩溃。
因此，**必须切换到 JTAG 模式**——该模式下 Flash 处于空闲状态，JTAG 可以自由访问 Flash 进行编程。

<a id="code2"> </a>

### 代码解释:Helloworld XDC

```tcl
# ==================================================
# 文件名：top.xdc 或 constraints.xdc
# 功能：定义设计中 GPIO_0_0_tri_io 总线两个比特对应的物理引脚位置和电平标准
# ==================================================

# ---------- 第 1 个引脚（索引 0）的约束 ----------
# 设置该引脚的 I/O 电平标准为 LVCMOS33
# LVCMOS33 = Low Voltage CMOS 3.3V，即 3.3V 逻辑电平。
# 这是常见标准，确保 FPGA 输出/输入电压与外部设备（如 LED、按键）匹配。
# [get_ports GPIO_0_0_tri_io[0]] 表示获取设计中名为 GPIO_0_0_tri_io 且索引为 0 的端口。
# 端口名中的 tri 通常表示三态 (tri-state) 双向 GPIO。
set_property IOSTANDARD LVCMOS33 [get_ports GPIO_0_0_tri_io[0]]

# 将该引脚分配到芯片封装上的物理球/引脚，编号为 P20
# 具体引脚号取决于芯片封装（例如 BGA 封装），不同芯片的 P20 位置不同。
# 该映射决定了 GPIO_0_0_tri_io[0] 实际连接到开发板/电路板的哪个焊盘。
set_property PACKAGE_PIN P20 [get_ports GPIO_0_0_tri_io[0]]

# ---------- 第 2 个引脚（索引 1）的约束 ----------
# 同样设置电平标准为 3.3V LVCMOS
set_property IOSTANDARD LVCMOS33 [get_ports GPIO_0_0_tri_io[1]]

# 分配到物理引脚 P21
set_property PACKAGE_PIN P21 [get_ports GPIO_0_0_tri_io[1]]
```

<a id="code1"> </a>

### 代码解释:Helloworld main.c

```c
/*
 * 文件名：main.c
 * 功能：基于 Zynq PS (Processing System) 的 GPIO 控制程序，实现两个 LED 灯同时闪烁。
 *       使用 Xilinx SDK 的 GPIOPS 驱动库，通过 PS 端的 MIO 引脚控制两个外部 LED。
 * 硬件平台：Xilinx Zynq-7000 系列（如 Zynq-7020）
 */

/* 包含 Xilinx 提供的硬件参数定义头文件，例如外设基地址、设备 ID 等 */
#include "xparameters.h"

/* 包含 GPIO PS (Processing System) 驱动库，用于控制 Zynq PS 端的 GPIO 引脚 */
#include "xgpiops.h"

/* 包含状态码定义（如 XST_SUCCESS），但本程序未显式使用，通常用于函数返回检查 */
#include "xstatus.h"

/* 包含平台信息相关函数（如获取 CPU 频率），本程序未使用，但保留为依赖 */
#include "xplatform_info.h"

/* 包含 sleep 函数（秒级延时），用于实现 LED 亮灭的可见间隔 */
#include "sleep.h"

/* 定义两个 LED 所连接的 MIO 引脚编号。
 * MIO (Multi-use I/O) 是 Zynq PS 端的固定引脚，可以直接控制外部设备。
 * 此处假设 LED1 连接 MIO54，LED2 连接 MIO55。
 */
#define LED1    54
#define LED2    55

/* 定义 GPIO 设备的 ID，对应 xparameters.h 中 XPAR_XGPIOPS_0_DEVICE_ID 的值。
 * Zynq PS 只有一个 GPIO 外设，其设备 ID 通常为 0。
 */
#define GPIO_DEVICE_ID  0

/* 声明一个 XGpioPs 结构体实例，用于表示 GPIO 外设。
 * 该结构体保存了 GPIO 外设的配置信息和运行时状态。
 */
XGpioPs Gpio;

/**
 * 函数名：Gpio_Init
 * 功能：初始化 GPIO 外设，将 LED1 和 LED2 对应的 MIO 引脚配置为输出模式，
 *       并初始化为低电平（熄灭状态）。
 * 参数：无
 * 返回值：无
 */
void Gpio_Init(void)
{
    /* 定义一个指向 XGpioPs_Config 结构体的指针，用于存储从查找函数返回的配置信息。
     * XGpioPs_Config 结构体包含外设的基地址、中断号等静态配置。
     */
    XGpioPs_Config *ConfigPtr;

    /* 根据设备 ID 查找 GPIO 外设的配置信息。
     * 参数 GPIO_DEVICE_ID 为 0，返回一个指向配置结构体的指针。
     * 如果查找失败（例如 ID 无效），返回值可能为 NULL，本例未做错误处理（初学者可简单使用）。
     */
    ConfigPtr = XGpioPs_LookupConfig(GPIO_DEVICE_ID);

    /* 使用查找到的配置信息初始化 GPIO 结构体实例 Gpio。
     * 第一个参数：指向要初始化的 XGpioPs 实例的指针
     * 第二个参数：配置结构体指针
     * 第三个参数：外设基地址（通常 ConfigPtr->BaseAddr 即为正确的基地址）
     * 该函数执行后，Gpio 结构体就代表了 GPIO 外设，后续函数均使用它操作硬件。
     */
    XGpioPs_CfgInitialize(&Gpio, ConfigPtr, ConfigPtr->BaseAddr);

    /* 设置 LED1 引脚的传输方向为输出。
     * 参数：
     *   - &Gpio: 指向已初始化的 GPIO 实例
     *   - LED1: 引脚编号 54
     *   - 1: 方向（1 表示输出，0 表示输入）
     */
    XGpioPs_SetDirectionPin(&Gpio, LED1, 1);

    /* 使能 LED1 引脚的输出功能。
     * 对于输出引脚，需要允许该引脚驱动外部电路（使能输出使能）。
     * 参数与 SetDirectionPin 类似，第三个参数为 1 表示允许输出。
     */
    XGpioPs_SetOutputEnablePin(&Gpio, LED1, 1);

    /* 同理，配置 LED2 引脚（MIO55）为输出模式 */
    XGpioPs_SetDirectionPin(&Gpio, LED2, 1);
    XGpioPs_SetOutputEnablePin(&Gpio, LED2, 1);

    /* 将 LED1 引脚输出低电平（0），使 LED 熄灭。
     * 注意：硬件电路通常设计为高电平点亮 LED，低电平熄灭。
     * 此处初始化为熄灭状态，避免上电后意外点亮。
     */
    XGpioPs_WritePin(&Gpio, LED1, 0);

    /* 将 LED2 引脚输出低电平，同样初始化为熄灭 */
    XGpioPs_WritePin(&Gpio, LED2, 0);
}

/**
 * 主函数：程序入口，执行 LED 循环闪烁功能。
 * 参数：无（标准嵌入式 main 函数通常不带参数）
 * 返回值：int 类型，理论上永远不会返回，因为 while(1) 无限循环。
 */
int main(void)
{
    /* 调用 GPIO 初始化函数，配置引脚并保证初始状态为熄灭 */
    Gpio_Init();

    /* 进入无限循环，实现两个 LED 同步闪烁 */
    while(1)
    {
        /* 两个 LED 同时熄灭（输出低电平） */
        XGpioPs_WritePin(&Gpio, LED1, 0);
        XGpioPs_WritePin(&Gpio, LED2, 0);

        /* 延时 1 秒，保持熄灭状态 */
        sleep(1);

        /* 两个 LED 同时点亮（输出高电平） */
        XGpioPs_WritePin(&Gpio, LED1, 1);
        XGpioPs_WritePin(&Gpio, LED2, 1);

        /* 延时 1 秒，保持点亮状态 */
        sleep(1);
    }

    /* 理论上永远不会执行到此，但为了满足 C 语言语法要求，返回 0 */
    return 0;
}
```

