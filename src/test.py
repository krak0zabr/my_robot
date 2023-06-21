#!/usr/bin/env python3
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16, Float32
from sensor_msgs.msg import LaserScan


class count():
    def __init__(self) -> None:
        #self.sub = rospy.Subscriber("/odom", Odometry, self.callback)
        #self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
        #self.tw = Twist()
        #self.od = Odometry()
        self.sub_scan = rospy.Subscriber("/scan", LaserScan, self.scan_callback)    
        self.pub_scan = rospy.Publisher("/edge", Float32, queue_size = 10)    

    def scan_callback(self, msg):
        i = 0
        min = 1000.0
        for i in range(len(msg.ranges)):
            if msg.ranges[i] > 0.13:
                if msg.ranges[i] < min:
                    min = msg.ranges[i]
                i += 1
        self.pub_scan.publish(min)
    
    

if __name__ == "__main__":
    rospy.init_node("dvijitel")
    co = count()
    rospy.spin()