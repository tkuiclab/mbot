#base topic info 

"linear:
  x: 0.0  -> x speed  -100~100
  y: 0.0  -> y speed  -100~100
  z: 0.0
angular:
  x: 0.0  -> cmd 0:speed mode, 1: enable, 2: stop
  y: 0.0
  z: 0.0" -> yaw speed -100~100


# base test
rosrun mbot_control base

---Speed Test---

rostopic pub /base_vel geometry_msgs/Twist "linear:
  x: 5.0
  y: 5.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"

---Stop Test---

rostopic pub /base_vel geometry_msgs/Twist "linear:
  x: 5.0
  y: 5.0
  z: 0.0
angular:
  x: 2.0
  y: 0.0
  z: 0.0"

---Enable Test---

rostopic pub /base_vel geometry_msgs/Twist "linear:
  x: 5.0
  y: 5.0
  z: 0.0
angular:
  x: 1.0
  y: 0.0
  z: 0.0"
