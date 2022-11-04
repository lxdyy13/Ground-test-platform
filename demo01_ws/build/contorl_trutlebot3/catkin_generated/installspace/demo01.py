#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def control_robot():
  pass
if __name__=="__main__":

    rospy.init_node('turtlebot3_teleop')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    while not rospy.is_shutdown():
        twist = Twist()

        #control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
        twist.linear.x = 1.0; twist.linear.y = 0.0; twist.linear.z = 0.0

        #control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0

        pub.publish(twist)

