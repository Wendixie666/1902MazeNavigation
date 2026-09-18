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

Run one command from the repository root. The script loads the ROS environment, sets the default robot model, and builds the workspace on the first run:

```bash
./run_maze.sh
```

Dynamic obstacles are disabled by default. Pass launch arguments through the script:

```bash
./run_maze.sh dynamic_obstacles:=true
```

For a headless environment:

```bash
./run_maze.sh gui:=false headless:=true
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
run_maze.sh                         # one-command simulation launcher
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
