# Docker / Dev Container 环境配置

本文从全新容器开始说明如何运行迷宫仿真。项目使用 ROS 1 Noetic、Ubuntu 20.04 和 Gazebo 11。ROS Noetic 已于 2025 年 5 月结束维护；这里保留该环境以运行现有课程项目。首次安装依赖需要网络连接。

## 方式一：VS Code Dev Container

主机需要安装 Docker、VS Code 和 VS Code 的 Dev Containers 扩展。打开本仓库，在命令面板中选择 **Dev Containers: Reopen in Container**。仓库的 `.devcontainer/devcontainer.json` 使用 `osrf/ros:noetic-desktop-full-focal` 镜像。

容器打开后，在仓库根目录的终端执行：

```bash
./install_dependencies.sh
./run_maze.sh gui:=false headless:=true
```

`install_dependencies.sh` 会安装 TurtleBot3、GMapping、导航、探索和 Gazebo 相关软件包，并运行 `catkin_make`。当前 Dev Container **不会自动执行**该脚本；每次重建为全新容器后需要重新安装。`run_maze.sh` 会加载 ROS 环境，并在尚未构建工作区时自动构建。

无界面模式无需把主机显示服务器接入容器，适合先验证仿真。需要 Gazebo 窗口时，可以运行 `./run_maze.sh`，但当前 Dev Container 没有配置显示转发；必须先根据主机系统配置容器的显示访问。Linux、Windows 和 macOS 的图形设置不同，不应把窗口能否弹出当作无界面仿真是否成功的判断依据。

## 方式二：直接使用 Docker CLI

不使用 VS Code 时，可在仓库根目录启动同一个基础镜像：

```bash
docker run --rm -it \
  --mount "type=bind,source=$(pwd),target=/workspace" \
  --workdir /workspace \
  docker.io/osrf/ros:noetic-desktop-full-focal bash
```

随后在容器内执行：

```bash
./install_dependencies.sh
./run_maze.sh gui:=false headless:=true
```

仓库以绑定挂载方式进入容器，因此构建结果会写入主机工作区的 `build/` 和 `devel/`。容器删除后，通过 `apt` 安装的软件包不会保留；新容器要重新执行依赖安装脚本。如果主机上已有其他 catkin 构建结果，先确认它们来自兼容的 Noetic 环境。

## 验证运行

安装后，可先确认关键软件包可见：

```bash
source /opt/ros/noetic/setup.bash
rospack find turtlebot3_gazebo
rospack find gmapping
rospack find move_base
rospack find explore_lite
```

启动仿真后，终端应显示机器人生成成功，`slam_gmapping` 开始处理激光扫描。在另一个容器终端中，可以检查话题：

```bash
source /opt/ros/noetic/setup.bash
source devel/setup.bash
rostopic list | grep -E '^/(scan|map|cmd_vel)$'
rostopic echo -n 1 /scan
```

首次构建和 Gazebo 启动可能需要一些时间。按 `Ctrl+C` 停止仿真。能看到 `/scan` 和 `/map` 说明传感器与建图链路已启动；还应继续观察导航日志，确认机器人能够持续探索。

## 常见问题

| 现象 | 检查方法 |
| --- | --- |
| `ROS Noetic was not found` | 确认使用上述 Noetic 镜像，或在本机安装 ROS Noetic。 |
| `Resource not found` / 找不到 ROS 包 | 先运行 `./install_dependencies.sh`，再用 `rospack find <包名>` 检查；手动运行 `roslaunch` 前还须加载 `devel/setup.bash`。 |
| Gazebo 窗口无法打开 | 先用 `gui:=false headless:=true` 验证仿真；当前容器配置没有显示转发。 |
| `NO PATH!` 反复出现 | 这是导航规划报错，不代表 Docker 安装失败；检查 `/scan`、`/map` 和代价地图，并记录启动日志以排查地图或规划参数。当前项目的短时无界面运行曾出现此报错。 |
| `apt` 下载失败 | 检查容器网络和软件源；Noetic 与 Ubuntu 20.04 已结束常规维护，旧软件源的可用性可能变化。 |

ROS Noetic 维护状态见 [ROS 公告](https://discourse.ros.org/t/ros-noetic-end-of-life-may-31-2025/43160)。Dev Container 的创建、重建机制见 [VS Code 官方文档](https://code.visualstudio.com/docs/devcontainers/create-dev-container)。
