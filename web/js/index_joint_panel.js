//Joint Control Panel
$('#control_send_joint').on('click',function(e){
	var float64 = new Float64Array(6);
	float64[0] = $('#input_j1').val()*(Math.PI/180);
	float64[1] = $('#input_j2').val()*(Math.PI/180);
	float64[2] = $('#input_j3').val()*(Math.PI/180);
	float64[3] = $('#input_j4').val()*(Math.PI/180);
	float64[4] = $('#input_j5').val()*(Math.PI/180);
	float64[5] = $('#input_j6').val()*(Math.PI/180);
	var send_joint = new ROSLIB.Message({
		cmd : 'Joint',
		joint_position : [float64[0],float64[1],float64[2],
				  float64[3],float64[4],float64[5]]
	});
	mlist.push(send_joint);
	// Create a goal.
	var goal = new ROSLIB.Goal({
		actionClient : teachModeClient,
		goalMessage : {
			cmd_list : mlist
		}
	});
	// Print out their output into the terminal.
	goal.on('feedback', function(feedback) {
		console.log('Feedback: ' + feedback.status);
	});
	goal.on('result', function(result) {
		console.log('Final Result: ' + result.notify);
	});
	// Send the goal to the action server.
	$("#infoContent").html('Goal was send cmdlist'
				+'<BR>Cmd : ' + send_joint.cmd
				+"<BR>Joint Position : [ "+ send_joint.joint_position+" ]"
	);
	goal.send();
	mlist = [];
});
