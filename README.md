# mbot
TKU Mobile Manipulator Robot (M-Bot)


#ur_Gazebo Setting
roslaunch ur_gazebo ur5.launch limited:=true
roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch sim:=true limited:=true
roslaunch ur5_moveit_config moveit_rviz.launch config:=true

#ur5
roslaunch ur_bringup ur5_bringup.launch limited:=true robot_ip:=192.168.137.5
roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch limited:=true
roslaunch ur5_moveit_config moveit_rviz.launch config:=true

#ur5_teach
roslaunch ur_bringup ur5_bringup.launch limited:=true robot_ip:=192.168.137.5 teach_mode:=true
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
$ sudo update-rc.d mini-httpd enable
$ sudo vim /etc/default/mini-httpd
START=1

