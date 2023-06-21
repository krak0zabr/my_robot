#!/usr/bin/env python3
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16, Float32
from my_robot.msg import point
from sensor_msgs.msg import LaserScan

class Square():
    def __init__(self) -> None:
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
        self.tw = Twist()
        self.pub_pose = rospy.Publisher("/goals", point, queue_size = 5)
        self.sub_odom = rospy.Subscriber("/odom", Odometry, self.callback_odom)
        self.od = Odometry()
        self.po = point()
        self.countt = 0
        self.sub_scan = rospy.Subscriber("/scan", LaserScan, self.callback_scan)    
        self.pub_scan = rospy.Publisher("/edge", Float32, queue_size = 10)
        
    def stop(self):
        self.tw.linear.x = 0
        self.tw.angular.z = 0
        rospy.sleep(1)
        self.pub.publish(self.tw)
    
    def forward(self):
        self.tw.linear.x = 0.35
        self.tw.angular.z = 0
        rospy.sleep(1)
        self.pub.publish(self.tw)
        rospy.sleep(2)

    def turn(self):
        self.tw.linear.x = 0
        self.tw.angular.z = 0.46
        rospy.sleep(1)
        self.pub.publish(self.tw)
        rospy.sleep(3)
    
    def callback_odom(self, message):
        self.pose_x = message.pose.pose.position.x
        self.pose_y = message.pose.pose.position.y
    
    def position(self):      #работает, но не правильно
        self.po.x = self.pose_x
        self.po.y = self.pose_y
        if self.countt == 1:
            self.po.inaccuracy = abs(self.po.x - 0.7) * 100
        if self.countt == 2:
            self.po.inaccuracy = abs(self.po.x - 0.7) * 100
        if self.countt == 3:
            self.po.inaccuracy = abs(self.po.x - 0) * 100
        if self.countt == 4:
            self.po.inaccuracy = abs(self.po.x - 0) * 100

        self.pub_pose.publish(self.po)
        self.countt += 1
        print(self.countt)

    def callback_scan(self, msg):
        i = 0
        min = 1000.0
        for i in range(len(msg.ranges)):
            if msg.ranges[i] > 0.13:
                if msg.ranges[i] < min:
                    min = msg.ranges[i]
                i += 1
        self.pub_scan.publish(min)
        
    def on(self):
        self.count = 0
        while self.count < 4:
            self.forward()
            self.stop()
            self.position()
            self.turn()
            self.count += 1
        self.stop()

if __name__ == "__main__":
    rospy.init_node("dvijitel")
    
    def callback(msg):
        sq = Square()
        sq.on()

    sub = rospy.Subscriber("/start", Int16, callback)
    rospy.spin()