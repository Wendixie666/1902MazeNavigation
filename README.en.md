# TurtleBot3 Maze Navigation

[简体中文](README.md)

This repository is a ROS 1 Noetic and Gazebo simulation project for autonomous TurtleBot3 exploration in a maze. In `maze22.world`, the robot builds a map from LiDAR and odometry, explores unknown areas, plans collision-free paths, and stops when its camera detects the green goal.

The project is intended for course experiments and algorithm demonstrations. It assembles existing ROS navigation components rather than implementing a new navigation stack.

## Core features

- GMapping SLAM builds an occupancy grid from `/scan` and `/odom`.
- `explore_lite` selects frontier regions and sends goals to `move_base`.
- `move_base` uses an A* global planner and DWA local planner.
- The Gazebo maze includes walls, a green goal, moving cylinder obstacles, and walking actors.
- The goal detector cancels navigation and stops the robot after five consecutive green detections.
- A standalone benchmark compares Dijkstra and A* path-planning costs.

## Quick start

Requirements: ROS Noetic, Gazebo, TurtleBot3 packages, and Python 3. The repository also includes a `.devcontainer/` configuration.

From the repository root:

```bash
source /opt/ros/noetic/setup.bash
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=waffle
roslaunch my_launch maze_exploration.launch
```

Dynamic obstacles are disabled by default. Enable them with:

```bash
roslaunch my_launch maze_exploration.launch dynamic_obstacles:=true
```

For a headless environment:

```bash
roslaunch my_launch maze_exploration.launch gui:=false headless:=true
```

## Navigation flow

```text
LiDAR + Odometry → GMapping → Occupancy Grid
                              ↓
       explore_lite → move_base (A* + DWA) → /cmd_vel
                              ↑
                   RGB Camera → Green Goal Detector
```

## Repository layout

```text
src/
├── my_launch/
│   ├── launch/maze_exploration.launch  # main simulation entry point
│   └── config/                         # SLAM, costmap, and planner parameters
└── my_maze_world/
    ├── worlds/maze22.world             # active maze world
    ├── models/                         # Gazebo models
    └── scripts/                        # obstacle, actor, and goal-detector nodes
```

## Planner benchmark

```bash
python3 src/my_maze_world/scripts/compare_planners.py
python3 src/my_maze_world/scripts/compare_planners.py --csv results.csv
```

The benchmark compares Dijkstra and A* on the same grid maze and reports path length, planning time, and expanded nodes.

