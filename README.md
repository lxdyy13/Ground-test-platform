# Ground-test-platform
turtlebot3 and NOKOV joint use
# 使用方法

## 机器人端： 

通过ssh远程启动机器人，在终端使用指令：

```
roslaunch turtlebot3_bringup turtlebot3_robot.launch
```

自己电脑需要安装ros环境 以及trutlebots相关包，使用命令：

```
sudo apt install ros-noetic-dynamixel-sdk

sudo apt install ros-noetic-turtlebot3-msgs

sudo apt install ros-noetic-turtlebot3
```



------



## PC端：

首先连接动捕使用命令：

```
roslaunch vrpn_client_ros sample.launch  server：=192.168.31.128
```

未安装vprn需要先安装vprn 使用命令：

```
sudo apt-get install ros-<your ros vision>-vrpn*
```

更新环境变量，使用命令：

```
source ./devel/setup.bash
```

把坐标点放入demo01.py文件里面的point数组中  

启动控制命令，有两种方式

控制机器人

```
rosrun control_robot control.py 
```

执行定点运行

```
rosrun control_robot demo01.py 
```


