# TurtleBot3 迷宫导航 / Maze Navigation with TurtleBot3

本仓库是一个基于 ROS 1 / Gazebo 的迷宫导航课程项目，保留了原始的
TurtleBot3 仿真和动态障碍物实验；它不是一个全新的导航栈实现。

This repository contains a ROS 1 / Gazebo maze-navigation course project. It
preserves the original TurtleBot3 simulation and its dynamic obstacle
experiments; it is not a new navigation-stack implementation.

## 项目内容 / What is included

- 基于 `maze22.world` 的 Gazebo 迷宫环境。
  A Gazebo maze environment based on `maze22.world`.
- 使用 `turtlebot3_description` 生成的 TurtleBot3。
  A TurtleBot3 spawned from `turtlebot3_description`.
- 通过 Gazebo 的 `/gazebo/set_model_state` 服务控制的三个移动圆柱障碍物。
  Three moving cylinder obstacles controlled through Gazebo's
  `/gazebo/set_model_state` service.
- 两个动画行走角色，每个角色由独立的 Python 节点控制。
  Two animated walking actors, each controlled by its own Python node.
- 使用 `/scan`、`/odom` 和标准 TurtleBot3 TF 链的 GMapping SLAM。
  GMapping SLAM using `/scan`, `/odom`, and the standard TurtleBot3 TF chain.
- 使用 `explore_lite` 进行前沿探索，并向 `move_base` 发送目标。
  `explore_lite` frontier exploration sending goals to `move_base`.
- 配置为使用 A* 的 `global_planner/GlobalPlanner`，其中 `use_dijkstra: false`。
  `global_planner/GlobalPlanner` configured for A* with `use_dijkstra: false`.
- 一个名为 `green_goal` 的绿色方块，以及一个在连续检测到绿色若干次后结束运行的 RGB 相机检测器。
  A green cube named `green_goal` and an RGB camera detector that ends the run
  after several consecutive green detections.

## 技术和运行环境 / Technology and environment

- ROS Noetic（ROS 1） / ROS Noetic (ROS 1)
- Ubuntu 20.04
- Gazebo
- TurtleBot3 软件包 / TurtleBot3 packages
- Python 3 和 `rospy` / Python 3 and `rospy`

仓库包含基于 `docker.io/osrf/ros:noetic-desktop-full-focal` 的 Dev Container 配置。
使用 VS Code 和 Dev Containers 扩展打开仓库，然后选择 **Reopen in Container**。
必须提前安装 Docker；如果需要 Gazebo 图形界面，容器还必须能够访问显示设备。

The repository includes a Dev Container configuration based on
`docker.io/osrf/ros:noetic-desktop-full-focal`. Open the repository in VS Code
with the Dev Containers extension and choose **Reopen in Container**. Docker
must already be installed and the container must have access to a display if
the Gazebo GUI is required.

## 构建和运行 / Build and run

在仓库根目录并进入 ROS Noetic 环境后执行：

From the repository root, inside the ROS Noetic environment:

```bash
source /opt/ros/noetic/setup.bash
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=waffle
roslaunch my_launch maze_exploration.launch
```

统一启动文件会启动 Gazebo、TurtleBot3、GMapping、`move_base`、`explore_lite` 和
绿色目标检测器。默认使用 `waffle` 模型是有意为之，因为其官方 Gazebo 描述提供了
检测器使用的 RGB-D 相机。为了验证导航链路，动态角色默认处于禁用状态；可以使用
以下命令启用：

The unified launch starts Gazebo, the TurtleBot3, GMapping, `move_base`,
`explore_lite`, and the green-goal detector. The default `waffle` model is
intentional because its official Gazebo description provides the RGB-D camera
used by the detector. Dynamic actors are disabled by default while validating
the navigation chain; enable them with:

```bash
roslaunch my_launch maze_exploration.launch dynamic_obstacles:=true
```

对于没有显示设备的容器，可以使用 `gui:=false headless:=true`。

For a display-less container, use `gui:=false headless:=true`.

算法流程如下：

The algorithm flow is:

```text
LiDAR + Odometry
        ↓
     GMapping
        ↓
 Occupancy Grid (/map)
        ↓
Frontier Exploration (explore_lite)
        ↓
    move_base
        ↓
Global Planner (A*) → Local Planner (DWA)
        ↓
     /cmd_vel
```

当 RGB 检测器在连续五帧中检测到绿色方块时，它会发布锁存的
`/green_goal_detected`，取消当前的 `move_base` 目标，停止 `explore_lite` 节点，
并持续发布零速度。

When the RGB detector sees the green cube in five consecutive frames, it
publishes latched `/green_goal_detected`, cancels the current move_base goal,
stops the `explore_lite` node, and continuously publishes zero velocity.

## 规划器性能对比 / Planner performance comparison

独立基准测试会在同一个四方向网格迷宫上比较 Dijkstra 和 A*，并报告路径长度、
规划时间、扩展节点数以及 Python 峰值内存分配：

The standalone benchmark compares Dijkstra and A* on the same four-direction
grid maze. It reports path length, planning time, expanded nodes, and peak
Python memory allocation:

```bash
python3 src/my_maze_world/scripts/compare_planners.py
python3 src/my_maze_world/scripts/compare_planners.py --csv results.csv
```

执行 `catkin_make` 后，也可以使用以下命令运行：

After `catkin_make`, it can also be run as:

```bash
rosrun my_maze_world compare_planners.py
```

## 项目结构 / Project layout

```text
.
├── .devcontainer/                 ROS Noetic Dev Container 配置 / definition
├── src/
│   ├── my_launch/                 启动文件包 / launch package
│   │   ├── config/                 导航参数 / navigation parameters
│   │   ├── launch/maze_exploration.launch
│   │   └── turtlebot3_empty_world.launch
│   └── my_maze_world/             世界、模型和 Python 节点 / worlds, models, and Python nodes
│       ├── models/
│       ├── scripts/
│       │   ├── dynamic_obstacles.py
│       │   ├── green_goal_detector.py
│       │   ├── person_walking.py
│       │   └── walking_person.py
│       └── worlds/
│           ├── maze11.world       较旧的备用迷宫 / older/alternate maze world
│           └── maze22.world       主启动文件使用的世界 / world used by the main launch file
└── LICENSE
```

## 重要文件 / Important files

- `maze_exploration.launch`：完整的自主探索入口。
  The complete autonomous exploration entry point.
- `turtlebot3_empty_world.launch`：仅启动 Gazebo 和机器人的基础启动文件。
  The Gazebo and robot-only base launch.
- `maze22.world`：当前使用的迷宫、绿色目标、三个占位障碍物模型和两个角色定义。
  The active maze, green goal, three placeholder obstacle
  models, and two actor definitions.
- `maze11.world`：为历史/参考用途保留；当前启动文件不会加载它。
  Retained for historical/reference purposes; it is not loaded
  by the current launch file.
- `dynamic_obstacles.py`：移动 `dynamic_obstacle_1`、`dynamic_obstacle_2` 和
  `dynamic_obstacle_3`。
  Moves `dynamic_obstacle_1`,
  `dynamic_obstacle_2`, and `dynamic_obstacle_3`.
- `walking_person.py`：移动 `walking_person` 角色。
  Moves the `walking_person` actor.
- `person_walking.py`：移动独立的 `person_walking` 角色。
  Moves the separate `person_walking` actor.
- `models/walkingperson` 和 `models/walking_person`：`maze22.world` 都需要这两个目录；
  目录名属于 Gazebo 模型 URI 的一部分。
  Both are required by
  `maze22.world`; their directory names are part of the Gazebo model URIs.

## 可复现性说明和限制 / Reproducibility notes and limitations

在 Noetic 容器中使用以下命令安装 ROS 二进制依赖：

Install the ROS binary dependencies in the Noetic container with:

```bash
apt-get update
apt-get install -y ros-noetic-turtlebot3 ros-noetic-turtlebot3-slam \
  ros-noetic-turtlebot3-navigation ros-noetic-slam-gmapping \
  ros-noetic-move-base ros-noetic-global-planner ros-noetic-map-server \
  ros-noetic-explore-lite ros-noetic-cv-bridge ros-noetic-image-transport \
  python3-opencv
```

运行行为取决于环境中可用的 ROS Noetic、Gazebo 和 TurtleBot3 版本。启动后请确认
`/scan`、`/odom`、`/map`、`/camera/rgb/image_raw` 和 `/move_base/status`。
可以使用以下命令检查当前启用的全局规划器：

The runtime behavior depends on the ROS Noetic, Gazebo, and TurtleBot3 versions
available in the environment. Verify `/scan`, `/odom`, `/map`,
`/camera/rgb/image_raw`, and `/move_base/status` while the launch is running.
The active global planner can be checked with:

```bash
rosparam get /move_base/base_global_planner
rosparam get /move_base/GlobalPlanner/use_dijkstra
```

预期值分别为 `global_planner/GlobalPlanner` 和 `false`。

The expected values are `global_planner/GlobalPlanner` and `false`.
