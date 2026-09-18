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

The repository does not contain a SLAM system, `move_base` configuration, or a
navigation algorithm. The robot is spawned in the simulation, but autonomous
navigation is outside the scope of this course project.

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
export TURTLEBOT3_MODEL=burger
roslaunch my_launch turtlebot3_empty_world.launch model:=${TURTLEBOT3_MODEL}
```

`burger` is the default model in the launch file. `waffle` and `waffle_pi` can
also be selected with the `model` launch argument if the corresponding
TurtleBot3 description is installed.

The main entry point is
`src/my_launch/turtlebot3_empty_world.launch`. It loads `maze22.world`, starts
Gazebo, spawns the robot, and starts all three obstacle/actor controllers.

## Project layout

```text
.
├── .devcontainer/                 ROS Noetic Dev Container definition
├── src/
│   ├── my_launch/                 launch package
│   │   └── turtlebot3_empty_world.launch
│   └── my_maze_world/             worlds, models, and Python nodes
│       ├── models/
│       ├── scripts/
│       │   ├── dynamic_obstacles.py
│       │   ├── person_walking.py
│       │   └── walking_person.py
│       └── worlds/
│           ├── maze11.world       older/alternate maze world
│           └── maze22.world       world used by the main launch file
└── LICENSE
```

## Important files

- `turtlebot3_empty_world.launch`: the current, recommended launch entry
  point.
- `maze22.world`: the active maze, three placeholder obstacle models, and two
  actor definitions.
- `maze11.world`: retained for historical/reference purposes; it is not loaded
  by the current launch file.
- `dynamic_obstacles.py`: moves `dynamic_obstacle_1`,
  `dynamic_obstacle_2`, and `dynamic_obstacle_3`.
- `walking_person.py`: moves the `walking_person` actor.
- `person_walking.py`: moves the separate `person_walking` actor.
- `models/walkingperson` and `models/walking_person`: both are required by
  `maze22.world`; their directory names are part of the Gazebo model URIs.

## Reproducibility notes and limitations

This is a preserved course-project simulation rather than a production ROS
package. The runtime behavior depends on the ROS Noetic, Gazebo, and TurtleBot3
versions available in the environment. The recommended reproducibility path is
the included Dev Container followed by `catkin_make`. Run the main launch file
with a working display when using Gazebo's GUI, and inspect the terminal logs
for service or model-loading errors.
