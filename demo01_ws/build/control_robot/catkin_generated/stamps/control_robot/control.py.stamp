#!/usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
import math

import sys, select, os
import tty, termios

# point=[ [1,1],
#         [1,1],
#         [1,1],
#         [1,2]
#       ]
point = [1,1]
pi=3.1415926535 

global yaw_real,angle_set,line_set,line_real

flag1=1
flag2=1
flag3=0

angle_last=0

num=1
# all_point=3
def motor(lx,az):
  # twist.linear.x = lx; twist.linear.y = ly; twist.linear.z = lz
  # twist.angular.x = ax; twist.angular.y = ay; twist.angular.z = az
  #去掉无关量 设置为0 前进控制为lx 角度控制为az
  twist.linear.x = lx; twist.linear.y = 0; twist.linear.z = 0
  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = az

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def key_control():
  key = getKey()
  if key == 'w' :
      motor(2,0) 
  elif key == 's' :
      motor(-2,0) 
  elif key == 'a' :
      motor(0,2) 
  elif key == 'd' :
      motor(0,-2) 
  elif key == ' ' or key == 's' :
      motor(0,0) 

def angle_real_cal(orientation_x,orientation_y,orientation_z,orientation_w):
  (r, p, y) = tf.transformations.euler_from_quaternion([orientation_x, orientation_y, orientation_z, orientation_w])
  y_r=y*(180/pi)
  rospy.loginfo("1111111111111111111111111111111111yaw_real:%f\n",y_r)
  return (r,p,y)

def angle_set_cal(x,y):
  angle_set1=math.atan2(y,x)
  #angle_set11=angle_set1*(180/pi)
  #rospy.loginfo("angle_set:%f",angle_set1)
  return angle_set1

def sqrt2(x,y):
  mid_x=x*x
  mid_y=y*y
  line_set1=math.sqrt(mid_x+mid_y)
  return line_set1

def robot_controller(line_set,line_real,angle_set,yaw_real,angle_set_last):
  global flag1,flag2,flag3 ,num

  yaw_real=yaw_real*(180/pi)
  angle_set=angle_set*(180/pi)
  # angle_set=angle_set*(180/pi)+angle_set_last

  yaw_real=abs(yaw_real)
  angle_set=abs(angle_set)
  
  rospy.loginfo("robot_contorl_yaw:%f",yaw_real)
  rospy.loginfo("robot_contorl_angle:%f",angle_set)
  # rospy.loginfo("angle_set_last:%f",angle_set_last)

  line_set=abs(line_set)
  line_real=abs(line_real)

  rospy.loginfo("robot_contorl_line_set:%f",line_set)
  rospy.loginfo("robot_contorl_line_real:%f\n",line_real)
  key_control()
  # if flag1:
  #   if(abs(angle_set-yaw_real)>1):
  #     motor(0,0.3)
  #     flag1=1
  #     flag2=0
  #     rospy.loginfo("flag1:%d,flag2:%d",flag1,flag2)
  #   else: 
  #     flag2=1
  #     flag1=0
  #     rospy.loginfo("flag1:%d,flag2:%d",flag1,flag2)
  # if flag2:
  #   if(abs(line_set-line_real)>0.08):
  #     motor(1,0)
  #     flag2=1
  #     rospy.loginfo("flag1:%d,flag2:%d",flag1,flag2)
  #   else:
  #     motor(0,0)
  #     flag2=0
  #     flag3=1
  #     rospy.loginfo("一轮结束\n")
  #   return flag3


def domsg(position_now):
  rospy.loginfo("position_x:%f",position_now.pose.position.x)
  rospy.loginfo("position_y:%f\n",position_now.pose.position.y)
  global twist
  global num
  global flag1 ,flag2 ,flag3
  global angle_last
  twist = Twist()

  # angle_set=angle_set_cal(point[num][0],point[num][1])
  ##优化 完成点对点的确定
  #angle_set=angle_set_cal(point[num][0]-point[num-1][0],point[num][1]-point[num-1][1])
  angle_set=angle_set_cal(point[0],point[1])
  (rool_real,pitch_real,yaw_real)=angle_real_cal(position_now.pose.orientation.x,position_now.pose.orientation.y,position_now.pose.orientation.z,position_now.pose.orientation.w)
  #ange=angle_set_cal_vpa(position_now.pose.position.x,position_now.pose.position.y)

  line_set=sqrt2(point[0],point[1])
  # rospy.loginfo("line_set:%f",line_set)
  line_real=sqrt2(position_now.pose.position.x,position_now.pose.position.y)
  # rospy.loginfo("line_real:%f\n",line_real)


  # power=robot_controller(line_set,line_real,angle_set,yaw_real,angle_last)
  power=robot_controller(line_set,line_real,angle_set,yaw_real,angle_last)
  if power:
    num+=1
    flag1=1
    flag2=0
    flag3=0
    power=0
  else:
    pass

  pub.publish(twist)
 

if __name__=="__main__":
  settings = termios.tcgetattr(sys.stdin)

  global twist
  twist = Twist()

  rospy.init_node('turtlebot3_teleop')
  pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
  sub=rospy.Subscriber("/vrpn_client_node/UGV_02/pose",PoseStamped,domsg,queue_size=1000)
  rospy.spin()

  #遥控控制模式
  # while not rospy.is_shutdown():
  #   key_control()
  #   pub.publish(twist)
 
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
