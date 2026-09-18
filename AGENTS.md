# Repository Guidelines

## Project Structure & Module Organization

This repository is a ROS 1 catkin workspace. The top-level `src/` directory contains:

- `my_maze_world/`: Gazebo worlds (`worlds/`), custom models (`models/`), and Python nodes for dynamic obstacles and walking people (`scripts/`).
- `my_launch/`: launch files for the TurtleBot3 and maze simulation.
- `.devcontainer/`: reproducible ROS Noetic development environment definition.

There is no committed `test/` directory or automated test suite. Treat simulation runs as the primary integration check.

## Build, Test, and Development Commands

Run from the repository root after sourcing the ROS distribution (for example, `source /opt/ros/noetic/setup.bash`):

```bash
catkin_make                         # Build all packages in this workspace
source devel/setup.bash             # Load the generated package environment
roslaunch my_launch turtlebot3_empty_world.launch
```

The launch file starts Gazebo with `maze22.world`, spawns a TurtleBot3, and runs the dynamic obstacle nodes. Use `rosrun my_maze_world dynamic_obstacles.py` only when testing that node independently. Confirm that Gazebo starts, the robot spawns, and obstacles move without repeated ROS service errors.

## Coding Style & Naming Conventions

Keep Python compatible with the repository’s ROS 1 Python 3 setup. Use four-space indentation, `snake_case` for functions and variables, and descriptive ROS node names. Preserve executable permissions and the `#!/usr/bin/env python3` shebang for scripts. Use XML indentation consistent with the existing launch files. Keep world/model names synchronized across `.world`, launch, and Python files.

## Testing Guidelines

Before submitting changes to worlds, models, launch files, or motion logic, run the relevant launch file and inspect Gazebo behavior and terminal logs. For Python-only changes, exercise affected trajectories or service calls in a live simulation. Record any required ROS packages or environment variables in the change description.

## Commit & Pull Request Guidelines

Existing commits use short, imperative-style descriptions, sometimes in Chinese (for example, `更新 maze22.world 文件`). Keep commits focused and describe the changed package or behavior. Pull requests should explain the scenario tested, list launch commands used, note environment assumptions, and include screenshots or logs when simulation visuals or runtime behavior changes.

## Configuration Notes

Prefer package-relative paths such as `$(find my_maze_world)` in launch files. Avoid introducing machine-specific absolute paths; review existing launch paths when modifying or reusing them.
