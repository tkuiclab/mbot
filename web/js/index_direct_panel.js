//Direct Control Button
//cause there has a lot of button need to send the value each other,so move this js code stand out the index.js
var speedArr;
var default_speed = 50;
$('#direction_speed_send').on('click',function(e){
	if(document.getElementById('direction_speed_value').value >=0 && document.getElementById('direction_speed_value').value<=100){
		default_speed = document.getElementById('direction_speed_value').value / 1;
		document.getElementById('direction_speed_value').value = '';
		document.getElementById('direction_speed_value').placeholder = default_speed * 1;
	}else{
		alert("Speed only allow 0~100%");
	}
});
function direct(dirID,spArr){
	$(dirID).on('mousedown',function(e){
//		var float64 = returnArray6(spArr[0],spArr[1],spArr[2],spArr[3],spArr[4],spArr[5]);
		var twist = new ROSLIB.Message({
			linear : {
			x : spArr[0]*default_speed,
			y : spArr[1]*default_speed,
			z : spArr[2]*default_speed
			},
			angular : {
			x : spArr[3]*default_speed,
			y : spArr[4]*default_speed,
			z : spArr[5]*default_speed
			}
		});
		direct_Pub.publish(twist);
		$("#infoContent").html('Topic was send twist'
					+"<BR>linear:<BR>"+ twist.linear.x +"<BR>"+ twist.linear.y +"<BR>"+ twist.linear.z
					+"<BR>angular<BR>"+ twist.angular.x +"<BR>"+ twist.angular.y +"<BR>"+ twist.angular.z
		);console.log(twist.linear.x+":"+twist.linear.y+":"+twist.linear.z);
	});
	//when mouseUp stop the motion
	$(dirID).on('mouseup',function(e){
		var twist = new ROSLIB.Message({
			linear : {x : 0,y : 0,z : 0},
			angular : {x : 0,y : 0,z : 0}
		});
		direct_Pub.publish(twist);
		$("#infoContent").html('Topic was send twist'
					+"<BR>linear:<BR>"+ twist.linear.x +"<BR>"+ twist.linear.y +"<BR>"+ twist.linear.z
					+"<BR>angular<BR>"+ twist.angular.x +"<BR>"+ twist.angular.y +"<BR>"+ twist.angular.z
		);
	});
}
speedArr = [ 0, 0, 1, 0, 0, 0];
direct("#direction_up",speedArr);
speedArr = [ 0, 0,-1, 0, 0, 0];
direct("#direction_down",speedArr);
speedArr = [ 0, 1, 0, 0, 0, 0];
direct("#direction_front",speedArr);
speedArr = [ 0,-1, 0, 0, 0, 0];
direct("#direction_back",speedArr);
speedArr = [ 1, 0, 0, 0, 0, 0];
direct("#direction_right",speedArr);
speedArr = [-1, 0, 0, 0, 0, 0];
direct("#direction_left",speedArr);

speedArr = [ 0, 0, 0, 0, 0,-1];
direct("#direction_yaw_left",speedArr);
speedArr = [ 0, 0, 0, 0, 0, 1];
direct("#direction_yaw_right",speedArr);
speedArr = [ 0, 0, 0, 1, 0, 0];
direct("#direction_pitch_up",speedArr);
speedArr = [ 0, 0, 0,-1, 0, 0];
direct("#direction_pitch_down",speedArr);
speedArr = [ 0, 0, 0, 0, 1, 0];
direct("#direction_roll_right",speedArr);
speedArr = [ 0, 0, 0, 0,-1, 0];
direct("#direction_roll_left",speedArr);
