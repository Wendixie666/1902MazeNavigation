#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ros_setup="/opt/ros/noetic/setup.bash"

if [[ ! -f "$ros_setup" ]]; then
    echo "ROS Noetic was not found at $ros_setup" >&2
    exit 1
fi

source "$ros_setup"
export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-waffle}"

if [[ ! -f "$workspace_dir/devel/setup.bash" ]]; then
    echo "Workspace is not built; running catkin_make..."
    (cd "$workspace_dir" && catkin_make)
fi

source "$workspace_dir/devel/setup.bash"
exec roslaunch my_launch maze_exploration.launch "$@"
