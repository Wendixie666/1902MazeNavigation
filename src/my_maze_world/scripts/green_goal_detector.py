#!/usr/bin/env python3
import subprocess

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from actionlib_msgs.msg import GoalID


class GreenGoalDetector:
    def __init__(self):
        image_topic = rospy.get_param('~image_topic', '/camera/rgb/image_raw')
        self.min_area = rospy.get_param('~min_area', 500)
        self.required_frames = rospy.get_param('~required_frames', 5)
        self.bridge = CvBridge()
        self.detected_frames = 0
        self.stopped = False

        self.detected_pub = rospy.Publisher(
            '/green_goal_detected', Bool, queue_size=1, latch=True)
        self.cancel_pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber(image_topic, Image, self.image_callback, queue_size=1)
        rospy.Timer(rospy.Duration(0.1), self.stop_callback)

        rospy.loginfo('Green goal detector listening on %s', image_topic)

    def image_callback(self, message):
        if self.stopped:
            return

        try:
            image = self.bridge.imgmsg_to_cv2(message, 'bgr8')
        except CvBridgeError as error:
            rospy.logwarn_throttle(5.0, 'Cannot convert camera image: %s', error)
            return

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (35, 80, 60), (85, 255, 255))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_area = 0.0
        for contour in contours:
            largest_area = max(largest_area, cv2.contourArea(contour))

        if largest_area >= self.min_area:
            self.detected_frames += 1
        else:
            self.detected_frames = 0

        if self.detected_frames >= self.required_frames:
            self.finish()

    def finish(self):
        self.stopped = True
        self.detected_pub.publish(Bool(data=True))
        self.cancel_pub.publish(GoalID())
        rospy.sleep(0.2)
        self.cancel_pub.publish(GoalID())

        subprocess.Popen(
            ['rosnode', 'kill', '/explore'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        rospy.loginfo('Green goal detected. Exploration finished.')

    def stop_callback(self, _event):
        if self.stopped:
            self.cmd_vel_pub.publish(Twist())


def main():
    rospy.init_node('green_goal_detector')
    GreenGoalDetector()
    rospy.spin()


if __name__ == '__main__':
    main()
