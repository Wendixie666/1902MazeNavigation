#!/usr/bin/env bash
set -eo pipefail

workspace_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ros_setup="/opt/ros/noetic/setup.bash"

if [[ ! -f "$ros_setup" ]]; then
    echo "ROS Noetic was not found at $ros_setup" >&2
    exit 1
fi

# Load ROS Noetic environment.
# Do this before enabling `set -u`, because ROS setup scripts may
# reference environment variables that have not been defined yet.
source "$ros_setup"

set -u

export ROS_MASTER_URI="${ROS_MASTER_URI:-http://localhost:11311}"
export ROS_HOSTNAME="${ROS_HOSTNAME:-localhost}"
export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-waffle}"
export LIBGL_ALWAYS_SOFTWARE=1

# Build the catkin workspace on first run.
if [[ ! -f "$workspace_dir/devel/setup.bash" ]]; then
    echo "Workspace is not built; running catkin_make..."
    (
        cd "$workspace_dir"
        catkin_make
    )
fi

# Load packages from this workspace.
source "$workspace_dir/devel/setup.bash"

echo "Starting TurtleBot3 maze exploration..."
echo "Workspace: $workspace_dir"
echo "TurtleBot3 model: $TURTLEBOT3_MODEL"

exec roslaunch my_launch maze_exploration.launch "$@"
