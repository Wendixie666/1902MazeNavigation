#!/usr/bin/env python3
"""
Walking person (actor) controller for maze navigation.
Controls the actor's position along a predefined path at 15 Hz.
The actor animates automatically via the DAE file, this script just moves it.
"""
import rospy
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose, Twist, Quaternion
import math

def linear_interpolate(start, end, period, t):
    """Linear interpolation between start and end positions"""
    tau = (t % period) / period
    x = start[0] + (end[0] - start[0]) * tau
    y = start[1] + (end[1] - start[1]) * tau
    z = start[2] + (end[2] - start[2]) * tau
    return x, y, z

def get_yaw_from_points(start, end):
    """Calculate yaw angle to face the direction of movement"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return 0
    return math.atan2(dy, dx)

def quaternion_from_yaw(yaw):
    """Convert yaw angle to quaternion"""
    half_yaw = yaw / 2.0
    qw = math.cos(half_yaw)
    qx = 0.0
    qy = 0.0
    qz = math.sin(half_yaw)
    return qw, qx, qy, qz

def scale_point(point, scale):
    return point[0] * scale, point[1] * scale, point[2]

def main():
    rospy.init_node('walking_person_mover')
    rospy.wait_for_service('/gazebo/set_model_state')
    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

    # target update rate (slowed to match other obstacles)
    rate_hz = rospy.get_param('~rate', 8.0)
    rate = rospy.Rate(rate_hz)
    maze_scale = rospy.get_param('~maze_scale', 0.5)

    # Keep the loop in the open area east of the maze walls.
    seg1_start = scale_point((7.8, 4.0, 0.85), maze_scale)
    seg1_end = scale_point((7.8, 8.0, 0.85), maze_scale)
    seg1_period = 8.0

    seg2_start = scale_point((7.8, 8.0, 0.85), maze_scale)
    seg2_end = scale_point((9.2, 8.0, 0.85), maze_scale)
    seg2_period = 4.0

    seg3_start = scale_point((9.2, 8.0, 0.85), maze_scale)
    seg3_end = scale_point((9.2, 4.0, 0.85), maze_scale)
    seg3_period = 8.0

    seg4_start = scale_point((9.2, 4.0, 0.85), maze_scale)
    seg4_end = scale_point((7.8, 4.0, 0.85), maze_scale)
    seg4_period = 4.0

    segments = [
        (seg1_start, seg1_end, seg1_period),
        (seg2_start, seg2_end, seg2_period),
        (seg3_start, seg3_end, seg3_period),
        (seg4_start, seg4_end, seg4_period),
    ]
    
    total_period = sum(p for _, _, p in segments)
    start_time = rospy.Time.now().to_sec()

    rospy.loginfo('walking_person_mover started (rate: %.1f Hz, total cycle: %.1f s)', rate_hz, total_period)
    rospy.loginfo('Actor will navigate through maze without colliding with walls')

    while not rospy.is_shutdown():
        now = rospy.Time.now().to_sec() - start_time
        cycle_time = now % total_period
        
        # Find which segment we're in
        current_pos = (7.8, 4.0, 0.85)
        current_yaw = 0
        elapsed = 0
        
        for start, end, period in segments:
            if elapsed + period > cycle_time:
                # We're in this segment
                time_in_segment = cycle_time - elapsed
                current_pos = linear_interpolate(start, end, period, time_in_segment)
                current_yaw = get_yaw_from_points(start, end)
                break
            elapsed += period

        # Create and send model state for the actor
        qw, qx, qy, qz = quaternion_from_yaw(current_yaw)
        
        ms = ModelState()
        ms.model_name = 'walking_person'
        ms.pose = Pose()
        ms.pose.position.x = current_pos[0]
        ms.pose.position.y = current_pos[1]
        # lock Z to maze ground plane
        ms.pose.position.z = 0.0
        ms.pose.orientation = Quaternion()
        ms.pose.orientation.w = qw
        ms.pose.orientation.x = qx
        ms.pose.orientation.y = qy
        ms.pose.orientation.z = qz
        ms.twist = Twist()
        ms.reference_frame = 'world'
        
        try:
            set_state(ms)
        except rospy.ServiceException as e:
            rospy.logwarn('set_model_state failed: %s', e)

        rate.sleep()

if __name__ == '__main__':
    main()
