# Maze Navigation with TurtleBot3

This repository contains a ROS 1 / Gazebo maze-navigation course project. It
preserves the original TurtleBot3 simulation and its dynamic obstacle
experiments; it is not a new navigation-stack implementation.

## What is included

- A Gazebo maze environment based on `maze22.world`.
- A TurtleBot3 spawned from `turtlebot3_description`.
- Three moving cylinder obstacles controlled through Gazebo's
  `/gazebo/set_model_state` service.
- Two animated walking actors, each controlled by its own Python node.
- GMapping SLAM using `/scan`, `/odom`, and the standard TurtleBot3 TF chain.
- `explore_lite` frontier exploration sending goals to `move_base`.
- `global_planner/GlobalPlanner` configured for A* with `use_dijkstra: false`.
- A green cube named `green_goal` and an RGB camera detector that ends the run
  after several consecutive green detections.

## Technology and environment

- ROS Noetic (ROS 1)
- Ubuntu 20.04
- Gazebo
- TurtleBot3 packages
- Python 3 and `rospy`

The repository includes a Dev Container configuration based on
`docker.io/osrf/ros:noetic-desktop-full-focal`. Open the repository in VS Code
with the Dev Containers extension and choose **Reopen in Container**. Docker
must already be installed and the container must have access to a display if
the Gazebo GUI is required.

## Build and run

From the repository root, inside the ROS Noetic environment:

```bash
source /opt/ros/noetic/setup.bash
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=waffle
roslaunch my_launch maze_exploration.launch
```

The unified launch starts Gazebo, the TurtleBot3, GMapping, `move_base`,
`explore_lite`, and the green-goal detector. The default `waffle` model is
intentional because its official Gazebo description provides the RGB-D camera
used by the detector. Dynamic actors are disabled by default while validating
the navigation chain; enable them with:

```bash
roslaunch my_launch maze_exploration.launch dynamic_obstacles:=true
```

For a display-less container, use `gui:=false headless:=true`.

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

When the RGB detector sees the green cube in five consecutive frames, it
publishes latched `/green_goal_detected`, cancels the current move_base goal,
stops the `explore_lite` node, and continuously publishes zero velocity.

## Project layout

```text
.
├── .devcontainer/                 ROS Noetic Dev Container definition
├── src/
│   ├── my_launch/                 launch package
│   │   ├── config/                 navigation parameters
│   │   ├── launch/maze_exploration.launch
│   │   └── turtlebot3_empty_world.launch
│   └── my_maze_world/             worlds, models, and Python nodes
│       ├── models/
│       ├── scripts/
│       │   ├── dynamic_obstacles.py
│       │   ├── green_goal_detector.py
│       │   ├── person_walking.py
│       │   └── walking_person.py
│       └── worlds/
│           ├── maze11.world       older/alternate maze world
│           └── maze22.world       world used by the main launch file
└── LICENSE
```

## Important files

- `maze_exploration.launch`: the complete autonomous exploration entry point.
- `turtlebot3_empty_world.launch`: the Gazebo and robot-only base launch.
- `maze22.world`: the active maze, green goal, three placeholder obstacle
  models, and two actor definitions.
- `maze11.world`: retained for historical/reference purposes; it is not loaded
  by the current launch file.
- `dynamic_obstacles.py`: moves `dynamic_obstacle_1`,
  `dynamic_obstacle_2`, and `dynamic_obstacle_3`.
- `walking_person.py`: moves the `walking_person` actor.
- `person_walking.py`: moves the separate `person_walking` actor.
- `models/walkingperson` and `models/walking_person`: both are required by
  `maze22.world`; their directory names are part of the Gazebo model URIs.

## Reproducibility notes and limitations

Install the ROS binary dependencies in the Noetic container with:

```bash
apt-get update
apt-get install -y ros-noetic-turtlebot3 ros-noetic-turtlebot3-slam \
  ros-noetic-turtlebot3-navigation ros-noetic-slam-gmapping \
  ros-noetic-move-base ros-noetic-global-planner ros-noetic-map-server \
  ros-noetic-explore-lite ros-noetic-cv-bridge ros-noetic-image-transport \
  python3-opencv
```

The runtime behavior depends on the ROS Noetic, Gazebo, and TurtleBot3 versions
available in the environment. Verify `/scan`, `/odom`, `/map`,
`/camera/rgb/image_raw`, and `/move_base/status` while the launch is running.
The active global planner can be checked with:

```bash
rosparam get /move_base/base_global_planner
rosparam get /move_base/GlobalPlanner/use_dijkstra
```

The expected values are `global_planner/GlobalPlanner` and `false`.
