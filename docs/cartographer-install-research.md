# Cartographer 在本项目容器中的安装调研

调研时间：2026-09-18

## 结论

本项目使用 Ubuntu 20.04、ROS 1 Noetic 和 Docker 基础镜像
`osrf/ros:noetic-desktop-full-focal`。Cartographer ROS 官方文档明确支持
Noetic，但推荐的安装方式是从源码构建，而不是依赖一个现成的 Noetic
二进制包。

推荐顺序：

1. 在容器内创建项目专用的独立 `cartographer_ws`，不要把上游源码直接混进
   当前项目的 `src/`。
2. 使用官方 `cartographer_ros.rosinstall` 拉取 `cartographer` 和
   `cartographer_ros`，用 `rosdep` 安装依赖，再用官方的 Abseil 脚本和
   `catkin_make_isolated --install --use-ninja` 编译。
3. 验证成功后，再把相同步骤固化进本项目的 `.devcontainer/Dockerfile`，从而
   让重建容器时自动获得 Cartographer。

## 现成包和现成 Docker 方案

- 当前 ROS Index 的 `cartographer_ros` 页面没有 Noetic 版本；页面末尾也明确
  提示没有 Noetic 版本。ROS 的 Kinetic/Noetic 对比页中，Cartographer 的
  `0.2.0` 条目只显示在 Kinetic 列，Noetic 列为空。因此当前容器不应假设
  `ros-noetic-cartographer` 或 `ros-noetic-cartographer-ros` 一定能通过 apt
  安装。
- 上游仓库提供了 `Dockerfile.noetic`，它以 `osrf/ros:noetic-desktop` 为基础，
  安装编译工具并从源码构建 Cartographer。这是可复用的官方构建配方，但不是
  一个已经包含 Cartographer 的现成镜像；它默认跟随 `master`，用于项目时应
  固定提交或版本。
- 当前容器的本地检查结果：Cartographer 四个 ROS 包均未安装，且 `git`、
  `ninja`、`stow` 缺失；`wstool`、`rosdep` 和 `catkin_make_isolated` 已有。

## 官方源码构建流程

官方 Noetic 文档给出的关键流程如下。容器内是 root 用户时可以去掉 `sudo`：

```bash
source /opt/ros/noetic/setup.bash

apt-get update
apt-get install -y git python3-wstool python3-rosdep ninja-build stow

mkdir -p /workspaces/AIE1902mid__MazeNavigation_Wendy/cartographer_ws/src
cd /workspaces/AIE1902mid__MazeNavigation_Wendy/cartographer_ws
wstool init src
wstool merge -t src \
  https://raw.githubusercontent.com/cartographer-project/cartographer_ros/master/cartographer_ros.rosinstall
wstool update -t src

rosdep init                 # 已初始化时出现错误可忽略
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro=noetic -y

src/cartographer/scripts/install_abseil.sh
catkin_make_isolated --install --use-ninja

source install_isolated/setup.bash
```

官方文档特别指出：Cartographer 使用的 Abseil 版本可能和 ROS 的
`abseil-cpp` 冲突；必要时需要移除 `ros-noetic-abseil-cpp` 后重新构建。应先
按实际构建错误决定，不建议一开始就删除系统包。

## 对本项目的实际影响

安装二进制只是获得节点，不会自动完成建图。当前项目还需要：

- TurtleBot3 的 `/scan` 激光数据；
- 从传感器到机器人坐标系的 TF，以及通常的里程计/IMU 数据；
- Cartographer 的 Lua 配置文件和启动文件；
- 运行时启动 `cartographer_node` 和占据栅格发布节点；
- 让机器人实际移动。当前主 launch 主要启动 Gazebo、机器人和动态障碍物，
  没有完整的 SLAM 启动配置。

首次验证应先关闭动态障碍物，只在静态迷宫中用键盘控制机器人移动，确认
`/scan`、TF、里程计和地图发布正常后，再恢复动态障碍物。动态障碍物会降低
建图质量，但不是 Cartographer 安装问题。

## 难度评估

源码编译本身属于中等难度：官方流程已经处理了大多数依赖，但 Abseil、Ceres
和系统库版本可能造成编译错误；编译时间和磁盘占用也明显高于直接安装普通
ROS 节点。真正需要较多项目工作的是把 TurtleBot3 仿真的传感器、TF、里程计和
Lua 配置接起来。

如果目标只是快速在这个 2D Gazebo 迷宫里出地图，ROS Noetic 的
`slam_gmapping` 通常更容易通过 apt 获得；如果课程/实验明确要求
Cartographer，则建议坚持上面的官方源码方案，不要换成第三方预编译镜像。

## 一手来源

- [Cartographer ROS 官方编译文档](https://github.com/cartographer-project/cartographer_ros/blob/master/docs/source/compilation.rst)
- [官方 Noetic Dockerfile](https://github.com/cartographer-project/cartographer_ros/blob/master/Dockerfile.noetic)
- [官方源码工作区清单](https://github.com/cartographer-project/cartographer_ros/blob/master/cartographer_ros.rosinstall)
- [Cartographer ROS 官方 README](https://github.com/cartographer-project/cartographer_ros)
- [ROS Index：cartographer_ros](https://index.ros.org/p/cartographer_ros/)
- [ROS Kinetic/Noetic 包状态对比](https://repositories.ros.org/status_page/compare_kinetic_noetic.html)
- [Cartographer 官方仓库维护状态说明](https://github.com/cartographer-project/cartographer)
