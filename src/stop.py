#!/usr/bin/env python3
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

rospy.init_node("dvijitel")

pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 11)
tw = Twist()
def movement():
    tw.linear.x = 0
    tw.angular.z = 0
    rospy.sleep(1)
    pub.publish(tw)
# rospy.sleep(7)
movement()
# tw.linear.x = 0
# tw.angular.z = 0
# rospy.sleep(1)
# pub.publish(tw)
###########################################################################################################################