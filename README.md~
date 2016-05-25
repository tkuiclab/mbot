# mbot
TKU Mobile Manipulator Robot (M-Bot)


#ur_Gazebo Setting
roslaunch ur_gazebo ur5.launch limited:=true

roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch sim:=true limited:=true

roslaunch ur5_moveit_config moveit_rviz.launch config:=true

#ur5
roslaunch ur_bringup ur5_bringup.launch limited:=true robot_ip:=192.168.5.5

roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch limited:=true

roslaunch ur5_moveit_config moveit_rviz.launch config:=true

#ur5_teach
roslaunch ur_bringup ur5_bringup.launch limited:=true robot_ip:=192.168.5.5 teach_mode:=true

roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch limited:=true

roslaunch ur5_moveit_config moveit_rviz.launch config:=true

# mbot_control
rosrun mbot_control teach_mode_server.py

rosrun mbot_control teach_mode_client.py  (test)



# rosbridge roslaunch
roslaunch rosbridge_server rosbridge_websocket.launch




# mini-httped Setting
1. Start 
$ sudo service mini-httpd start

2. Edit(if need)

$ sudo vim /etc/mini-httpd.conf

2.1. Edit path

data_dir=/home/iclab/mbot_ws/src/web

2.2. bind host(ip address)

host=[your ip] 

3. Auto Start
4. 
$ sudo update-rc.d mini-httpd enable

$ sudo vim /etc/default/mini-httpd

START=1


# ur control
roslaunch rosbridge_server rosbridge_websocket.launch

rosrun mbot_control info.py

rosrun mbot_control ur5_control.py


# base test
rosrun mbot_control base base_arduino

rostopic pub /base_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 3.0
  y: 2.0
  z: 0.0"

# ur5 with base
roslaunch rosbridge_server rosbridge_websocket.launch

rosrun mbot_control info.py


rosrun mbot_control base

rosrun mbot_control control.py

rosrun mbot_strategy strategy.py


直接開啟/home/mbot_ws/src/web/teach_mode.html

# ur5 with base(解說)
roslaunch rosbridge_server rosbridge_websocket.launch   (目的：可以使用網頁當介面)

rosrun mbot_control info.py			(目的：網頁跟本系統溝通的橋樑)

rosrun mbot_control control.py		(目的：mbot機器人控制)
	
rosrun mbot_control base			(目的：控制下面平台)





# urx install
sudo pip install math3d  (maybe you need to get pip -> #sudo apt-get install python-pip)

https://github.com/SintefRaufossManufacturing/python-urx   (download url)

python setup.py install



#config file
/home/mbot_ws/src/mbot_config/teach_mode.json

#debug 問題
#----Base debug----#
1. 出現下方訊息  代表RS232開啟失敗
問題：
(Base Node) Open RS232(/dev/ttyACM0)
cssl: cannot open file
(Base Node) Open RS232(/dev/ttyACM0) fail
(Base Node) Open RS232(/dev/ttyACM1)
(Base Node) Open RS232(/dev/ttyACM1) fail
解決：權限問題

#open camera
cd /usrcd/src/flycapture/bin
sudo FlyCap2

sudo FlyCap2

