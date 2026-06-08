# 系统更新和ROS2安装

## 更新源和软件包 确保没有垃圾软件包

```Plain Text
sudo apt update
sudo apt upgrade
sudo apt dist-upgrade
# 可选：清理无用包
sudo apt autoremove
# 重启
sudo reboot
```

## 卸载ROS1

ROS1与 Ubuntu22\.04 “不兼容” 

直接执行系统更新会被提示要求卸载ROS1

```Plain Text
# 卸载所有与ros-noetic相关的包
sudo apt purge ros-noetic-*
# 同时卸载ROS相关的Python 3包（Noetic主要使用Python 3）
sudo apt purge python3-ros*
```

## 更新系统

```Plain Text
# 启动升级管理器
sudo do-release-upgrade
```

系统更新前**务必备份资料** 有概率更新失败！

更新系统是会问你保留你修改的还是新的一些设置 推荐“Y”

## 安装ROS2 Humble

这边直接上鱼香ROS一键安装

```Plain Text
wget http://fishros.com/install -O fishros && . fishros
```

参考文档

- 系统更新

https://blog\.csdn\.net/wu\_weijie/article/details/124345707

- 一键安装

https://fishros\.org\.cn/forum/topic/20/%E5%B0%8F%E9%B1%BC%E7%9A%84%E4%B8%80%E9%94%AE%E5%AE%89%E8%A3%85%E7%B3%BB%E5%88%97

