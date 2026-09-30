# ROS2 系统状态监控 (ros2_sys_monitor)

本仓库为 2026 无人组招新笔试作业。

## 项目简介
包含两个 ROS2 功能包：
- **status_interfaces**: 自定义消息接口 `SystemStatus.msg`，包含时间、主机名、CPU、内存、网络等 8 个字段。
- **status_publisher**: Python 节点，负责采集系统状态并发布，同时使用 PyQt5 编写 GUI 窗口订阅并实时显示。

## 运行环境
- Ubuntu 22.04
- ROS 2 Humble
- Python 3.10

## 编译与运行
```bash
cd ~/ros2_ws
colcon build
source install/setup.bash

# 终端1：启动数据发布节点
ros2 run status_publisher sys_status_pub

# 终端2：启动Qt界面显示
ros2 run status_publisher sys_status_gui
