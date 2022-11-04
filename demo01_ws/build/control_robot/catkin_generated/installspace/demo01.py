#!/usr/bin/env python3

import rospy
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
import math

point=[
        [-1.6,-1.2],[-1.6,0],[-0.7,0],[0,0],[0.3,-1.2],[-0.6,-1.2],[-1.6,-1.2],[-1.6,0],[-1.6,1.5],[-0.5,1.6],[1,1.6],[0.7,0.8],[1.1,1.6],[1,1.6],[-0.5,1.6],[1,1.6],[0.7,0.8],[0,0],[-0.7,0],[0,0],[0.3,-1.2],[-0.6,-1.2],[-1.6,-1.2],[-1.6,0],[-0.7,0],[0,0],[1,0],[1.1,-1.2],[0.3,-1.2],[-0.6,-1.2],[-0.7,0],[-1.6,0],[-1.6,1.5],[-0.5,1.6],[1,1.6],[0.7,0.8],[1.1,1.6],[1,1.6],[-0.5,1.6],[-0.7,0],[0,0],[1,0],[2.1,1.6],[1.1,1.6],[1,1.6],[0.7,0.8],[0,0],[0.3,-1.2],[-0.6,-1.2],[-1.6,-1.2],[-1.6,0],[-0.7,0],[0,0],[1,0],[1.1,-1.2],[0.3,-1.2],[-0.6,-1.2],[-0.7,0],[-1.6,0],[-1.6,1.5],[-0.5,1.6],[1,1.6],[0.7,0.8],[1.1,1.6],[1,1.6],[-0.5,1.6],[-0.7,0],[0,0],[1,0],[1.1,-1.2],[0.3,-1.2],[-0.6,-1.2],[-1.6,-1.2],[-1.6,0],[-1.6,1.5],[-0.5,1.6],[1,1.6],[0.7,0.8],[0,0],[0.3,-1.2],[-0.6,-1.2],[-0.7,0],[0,0],[1,0],[2.1,1.6],[1.1,1.6],[1,1.6],[-0.5,1.6],[1,1.6],[0.7,0.8],[0,0],[0.3,-1.2],[-0.6,-1.2],[-1.6,-1.2],[-1.6,0],[-0.7,0],[0,0],[1,0],[1.1,-1.2]
      ]

pi=3.1415926535 
last_num=0
num=1
angle_flag=0
line_flag=0

flag_all_1=0
flag_all_2=0

class PID_init:
  def __init__(self) -> None:
    self.kp=0.0
    self.ki=0.0
    self.kd=0.0
    self.err=0.0
    self.output_minlimit=0.0
    self.output_maxlimit=0.0
    self.output_last=0.0
    self.output_llast=0.0
    self.output=0.0
    self.integral=0.0

def Normalization2(x):
  return 2*(x+65)/(65+65)-1

def motor(lx,az):
  # twist.linear.x = lx; twist.linear.y = ly; twist.linear.z = lz
  # twist.angular.x = ax; twist.angular.y = ay; twist.angular.z = az
  #去掉无关量 设置为0 前进控制为lx 角度控制为az
  twist.linear.x = lx; twist.linear.y = 0; twist.linear.z = 0
  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = az

def angle_real_cal(orientation_x,orientation_y,orientation_z,orientation_w):
  (r, p, y) = tf.transformations.euler_from_quaternion([orientation_x, orientation_y, orientation_z, orientation_w])
  y_r=y*(180/pi)
  rospy.loginfo("1111111111111111111111111111111111yaw_real:%f\n",y_r)
  return (r,p,y)

def angle_set_cal(x,y):
  angle_set=math.atan2(y,x)
  #angle_set11=angle_set1*(180/pi)
  #rospy.loginfo("angle_set:%f",angle_set1)
  return angle_set

def sqrt2(x,y):
  mid_x=x*x
  mid_y=y*y
  line_set1=math.sqrt(mid_x+mid_y)
  return line_set1

angle_pid_init=PID_init()
angle_pid_init.kp=1.0
angle_pid_init.ki=0.8
angle_pid_init.kd=40.0
angle_pid_init.err=0.0
angle_pid_init.output=0.0
angle_pid_init.output_minlimit=-1
angle_pid_init.output_maxlimit=1
angle_pid_init.output_last=0.0
angle_pid_init.output_llast=0.0
angle_pid_init.integral=0.0

def angle_pid(angle_set,angle_real):
  global angle_pid_init
  angle_pid_init.err=angle_set-angle_real
  angle_pid_init.integral=angle_pid_init.err+angle_pid_init.output_last
  angle_pid_init.output=angle_pid_init.kp*angle_pid_init.err+angle_pid_init.ki*(angle_pid_init.integral)+angle_pid_init.kd*(angle_pid_init.err-angle_pid_init.output_last)
  angle_pid_init.output_llast=angle_pid_init.output_last
  angle_pid_init.output_last=angle_pid_init.err
  rospy.loginfo("angle_pid_init.output:%f\n",angle_pid_init.output)
  #数据归一化
  angle_pid_init.output=Normalization2(angle_pid_init.output)
  return angle_pid_init.output

def angle_control(yaw_set,yaw_real):
  global angle_flag,line_flag,flag_all_2
  angle_set=yaw_set*(180/pi)
  angle_real=yaw_real*(180/pi)
  angle_flag=0
  angle_set_abs=abs(angle_set)
  angle_real_abs=abs(angle_real)
  rospy.loginfo("angle_set:%f",angle_set)
  rospy.loginfo("angle_real:%f",angle_real)
  # rospy.loginfo("angle_flagangle_flagangle_flag:%f",angle_flag)
  # rospy.loginfo("angle_set_abs-angle_set_abs:%f",angle_real_abs-angle_set_abs)
  if(abs(angle_real_abs-angle_set_abs)>3)&(angle_flag==0):
  #if((angle_set-angle_real)>5)&(angle_flag==0):
    out=angle_pid(angle_set,angle_real)
    rospy.loginfo("angle_out:%f\n",out)
    motor(0,out)
    line_flag=1
    flag_all_2=0
  else:
    line_flag=0
    flag_all_2=1
    rospy.loginfo("333333333333333333333333333333333")
    angle_flag=1
  return angle_flag

line_pid_init=PID_init()
line_pid_init.kp=5.0
line_pid_init.ki=0.0
line_pid_init.kd=8.0
line_pid_init.integral=0.0
line_pid_init.err=0.0
line_pid_init.output=0.0
line_pid_init.output_last=0.0
line_pid_init.output_llast=0.0
line_pid_init.output_minlimit=0
line_pid_init.output_maxlimit=2

def line_pid(line_target_set,line_target_real):
  global line_pid_init
  line_pid_init.err=line_target_set-line_target_real
  line_pid_init.integral=line_pid_init.err+line_pid_init.output_last
  line_pid_init.output=line_pid_init.kp*line_pid_init.err+line_pid_init.ki*(line_pid_init.integral)+line_pid_init.kd*(line_pid_init.err-line_pid_init.output_last)
  line_pid_init.output_llast=line_pid_init.output_last
  line_pid_init.output_last=line_pid_init.err
  rospy.loginfo("line_pid_init.output:%f\n",line_pid_init.output)
  #数据归一化
  line_pid_init.output=Normalization2(line_pid_init.output)+2
  return line_pid_init.output

def line_contorl(line_set1,line_real1):
  global line_flag,angle_flag,flag_all_1
  line_set=line_set1
  line_real=line_real1
  rospy.loginfo("line_set:%f",line_set)
  rospy.loginfo("line_real:%f",line_real)
  if (abs(line_real-line_set)>0.02)&(line_flag==0):
    out=line_pid(line_set,line_real)
    rospy.loginfo("out:%f\n",out)
    motor(out,0)
    angle_flag=1
    flag_all_1=0
  else:
    angle_flag=0
    flag_all_1=1
    line_flag=1
  return line_flag

def domsg(position_now):
  global line_flag,angle_flag,flag_all_2,flag_all_1
  global num,last_num
  rospy.loginfo("position_x:%f",position_now.pose.position.x)
  rospy.loginfo("position_y:%f\n",position_now.pose.position.y)
  global twist
  twist = Twist()

  ##优化 完成点对点的确定
  point_set_x_err=point[num][0]-point[last_num][0]
  point_set_y_err=point[num][1]-point[last_num][1]
  # point_set_x_err=1
  # point_set_y_err=1

  point_real_x_err=position_now.pose.position.x-point[last_num][0]
  point_real_y_err=position_now.pose.position.y-point[last_num][1]
  # point_real_x_err=position_now.pose.position.x
  # point_real_y_err=position_now.pose.position.y

  angle_set=angle_set_cal(point_set_x_err,point_set_y_err)
  (rool_real,pitch_real,yaw_real)=angle_real_cal(position_now.pose.orientation.x,position_now.pose.orientation.y,position_now.pose.orientation.z,position_now.pose.orientation.w)


  line_set=sqrt2(point_set_x_err,point_set_y_err)
  # rospy.loginfo("line_set:%f",line_set)
  line_real=sqrt2(point_real_x_err,point_real_y_err)
  #rospy.loginfo("line_real:%f",line_real)

  # rospy.loginfo("last_numlast_numlast_numlast_numlast_num:%f",last_num)
  # rospy.loginfo("numnumnumnumnum:%f",num)
  if num<5:
    flag=angle_control(angle_set,yaw_real)
    if flag:
      flag_insert=line_contorl(line_set,line_real)
      if flag_insert:
        if (flag_all_1==1)and(flag_all_2==1):
            last_num=num
            num+=1
            flag_all_1=0
            flag_all_2=0
    pub.publish(twist)
  else: num=0 

if __name__=="__main__":

  global twist
  twist = Twist()

  rospy.init_node('turtlebot3_control')
  pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

  sub=rospy.Subscriber("/vrpn_client_node/UGV_02/pose",PoseStamped,domsg,queue_size=1000)
  rospy.spin()

