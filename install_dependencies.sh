#!/usr/bin/env bash
set -eo pipefail

echo "======================================"
echo " Installing Maze Navigation dependencies"
echo "======================================"

# 支持 Docker root 用户，也支持普通 Ubuntu 用户
if [[ "$(id -u)" -eq 0 ]]; then
    APT="apt-get"
else
    if ! command -v sudo >/dev/null 2>&1; then
        echo "Error: need root permission or sudo."
        exit 1
    fi
    APT="sudo apt-get"
fi

# 检查 ROS Noetic
if [[ ! -f /opt/ros/noetic/setup.bash ]]; then
    echo "Error: ROS Noetic not found."
    echo "This project expects ROS Noetic / Ubuntu 20.04."
    exit 1
fi

source /opt/ros/noetic/setup.bash

echo
echo "[1/4] Updating apt package index..."
$APT update

echo
echo "[2/4] Installing ROS / TurtleBot3 dependencies..."

$APT install -y \
    git \
    python3-opencv \
    python3-rosdep \
    ros-noetic-turtlebot3 \
    ros-noetic-turtlebot3-msgs \
    ros-noetic-turtlebot3-simulations \
    ros-noetic-gmapping \
    ros-noetic-navigation \
    ros-noetic-explore-lite \
    ros-noetic-cv-bridge \
    ros-noetic-image-transport \
    ros-noetic-gazebo-ros \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-gazebo-ros-control

echo
echo "[3/4] Checking important ROS packages..."

packages=(
    turtlebot3_description
    turtlebot3_gazebo
    gmapping
    move_base
    explore_lite
    cv_bridge
)

failed=0

for package in "${packages[@]}"; do
    if rospack find "$package" >/dev/null 2>&1; then
        echo "  ✓ $package"
    else
        echo "  ✗ $package NOT FOUND"
        failed=1
    fi
done

echo
echo "[4/4] Building workspace..."

workspace_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cd "$workspace_dir"
catkin_make

echo
echo "======================================"

if [[ "$failed" -eq 0 ]]; then
    echo " All dependencies installed successfully."
    echo
    echo " Run the maze with:"
    echo
    echo "   ./run_maze.sh"
else
    echo " Installation finished, but some packages are missing."
    echo " Check the messages above."
fi

echo "======================================"