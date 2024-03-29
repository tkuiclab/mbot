// Connecting to ROS
// -----------------

var ros = new ROSLIB.Ros({
	url : 'ws://localhost:9090'
});

ros.on('connection', function() {
	console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
	console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
	console.log('Connection to websocket server closed.');
});
// The ActionClient
// ----------------
var teachModeClient = new ROSLIB.ActionClient({
	ros : ros,
	serverName : '/teach_mode_server',
	actionName : 'strategy/TeachCommandListAction'
});
// Subscribing to a Topic
// ----------------------
var joint_Sub = new ROSLIB.Topic({
	ros:ros,
	name: '/joint_states',
	messageType : 'sensor_msgs/JointState'
});
var eef_Sub = new ROSLIB.Topic({
	ros:ros,
	name: '/eef_states',
	messageType : 'geometry_msgs/Twist'
});

function saveBtn(){
	console.log("save Btn click");
}

$(document).ready(function(){
	$("#infoPanel").draggable();
	$("#ioPanel").draggable();
	//Detect mouse still down
	$('#direction_front').mousedown(function(e){
		mouseStillDown = true;
		doSomething();
	});
	var temp=1;
	function doSomething(){
		if (!mouseStillDown) {return;}
		else if (mouseStillDown) {
			console.log(temp++);
			setInterval(doSomething, 1000);
		}
	}
	$('#direction_front').mouseup(function(e){
		mouseStillDown = false;
		clearInterval(doSomething);
		temp=1;
	});
	//Panel_Edit
	$('#control_edit_joint').on('click',function(e){
		$('#dialog_table_joint').show();
		$('#dialog_table_eef').hide();
		$('#dialog_table_plus').hide();
	});
	$('#control_edit_eef').on('click',function(e){
		$('#dialog_table_eef').show();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').hide();
	});
	//ROS_Bridge
	$('#control_send_joint').on('click',function(e){
		var float64 = new Float64Array(6);
		float64[0] = $('#input_j1').val()*(Math.PI/180);
		float64[1] = $('#input_j2').val()*(Math.PI/180);
		float64[2] = $('#input_j3').val()*(Math.PI/180);
		float64[3] = $('#input_j4').val()*(Math.PI/180);
		float64[4] = $('#input_j5').val()*(Math.PI/180);
		float64[5] = $('#input_j6').val()*(Math.PI/180);
		var send_joint = new ROSLIB.Message({
			cmd : 'JointPosition',
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
	$('#control_send_eef').on('click',function(e){
		var float64 = new Float64Array(6);
		float64[0] = $('#input_lx').val();
		float64[1] = $('#input_ly').val();
		float64[2] = $('#input_lz').val();
		float64[3] = $('#input_ax').val();
		float64[4] = $('#input_ay').val();
		float64[5] = $('#input_az').val();
		var twist = new ROSLIB.Message({
			linear : {
			x : float64[0],
			y : float64[1],
			z : float64[2]
			},
			angular : {
			x : float64[3],
			y : float64[4],
			z : float64[5]
			}
		});
		var send_eef = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_eef);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		goal.on('feedback', function(feedback) {
			console.log('Feedback: ' + feedback.status);
		});
		goal.on('result', function(result) {
			console.log('Final Result: ' + result.notify);
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_eef.cmd +"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_eef.pose.linear.x +"<BR>"+ send_eef.pose.linear.y +"<BR>"+ send_eef.pose.linear.z
					+"<BR>angular<BR>"+ send_eef.pose.angular.x +"<BR>"+ send_eef.pose.angular.y +"<BR>"+ send_eef.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#control_io').on('click',function(e){
		if(io_default===false){
			io_default=true;
			$("#output_io").html('On');
			var send_io = new ROSLIB.Message({
				cmd : 'Vaccum',
				vaccum : true
			});
			mlist.push(send_io);
		}else{
			io_default=false;
			$("#output_io").html('Off');
			var send_io = new ROSLIB.Message({
				cmd : 'Vaccum',
				vaccum : false
			});
			mlist.push(send_io);
		}
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		goal.on('feedback', function(feedback) {
			console.log('Feedback: ' + feedback.status);
		});
		goal.on('result', function(result) {
			console.log('Final Result: ' + result.notify);
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_io.cmd
					+'<BR>Vaccum : '+ send_io.vaccum
		);
		goal.send();
		mlist = [];
	});
	$('#control_send_home').on('click',function(e){
		var float64 = new Float64Array(6);
		float64[0] = 0;
		float64[1] = -1.5708;
		float64[2] = 0;
		float64[3] = -1.5708;
		float64[4] = 0;
		float64[5] = 0;
		var send_joint = new ROSLIB.Message({
			cmd : 'JointPosition',
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
	//Panel control(use Left,Right,Plus,Minus button)
	
	//Dialog_send
	$('#control_send_eef_d').on('click',function(e){
		//console.log(('#table_test').children("tr:nth-child(1)").children("td:nth-child(1)").html('X'));
		var float64 = new Float64Array(6);
		float64[0] = $('#input_lx_d').val();
		float64[1] = $('#input_ly_d').val();
		float64[2] = $('#input_lz_d').val();
		float64[3] = $('#input_ax_d').val();
		float64[4] = $('#input_ay_d').val();
		float64[5] = $('#input_az_d').val();
		var twist = new ROSLIB.Message({
			linear : {
			x : float64[0],
			y : float64[1],
			z : float64[2]
			},
			angular : {
			x : float64[3],
			y : float64[4],
			z : float64[5]
			}
		});
		var send_eef = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_eef);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		goal.on('feedback', function(feedback) {
			console.log('Feedback: ' + feedback.status);
		});
		goal.on('result', function(result) {
			console.log('Final Result: ' + result.notify);
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_eef.cmd
					+'<BR>Vaccum : '+ send_eef.vaccum
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_eef.pose.linear.x
					+"<BR>"+ send_eef.pose.linear.y
					+"<BR>"+ send_eef.pose.linear.z
					+"<BR>angular<BR>"+ send_eef.pose.angular.x
					+"<BR>"+ send_eef.pose.angular.y
					+"<BR>"+ send_eef.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#control_send_joint_d').on('click',function(e){
		var float64 = new Float64Array(6);
		float64[0] = $('#input_j1_d').val()*(Math.PI/180);
		float64[1] = $('#input_j2_d').val()*(Math.PI/180);
		float64[2] = $('#input_j3_d').val()*(Math.PI/180);
		float64[3] = $('#input_j4_d').val()*(Math.PI/180);
		float64[4] = $('#input_j5_d').val()*(Math.PI/180);
		float64[5] = $('#input_j6_d').val()*(Math.PI/180);
		var send_joint = new ROSLIB.Message({
			cmd : 'JointPosition',
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
	//Topic_Subscribe
	joint_Sub.subscribe(function(message){
		//Show Progress-bar
//		document.getElementById('progress-bar_j1').style.width = ((((message.position[0]/Math.PI)*180)+360)/720)*100+'%';
		$("#progress-bar_j1").css({'width':((((message.position[0]/Math.PI)*180)+360)/720)*100+'%'});
		$("#progress-bar_j2").css({'width':((((message.position[1]/Math.PI)*180)+360)/720)*100+'%'});
		$("#progress-bar_j3").css({'width':((((message.position[2]/Math.PI)*180)+360)/720)*100+'%'});
		$("#progress-bar_j4").css({'width':((((message.position[3]/Math.PI)*180)+360)/720)*100+'%'});
		$("#progress-bar_j5").css({'width':((((message.position[4]/Math.PI)*180)+360)/720)*100+'%'});
		$("#progress-bar_j6").css({'width':((((message.position[5]/Math.PI)*180)+360)/720)*100+'%'});

		$("#output_j1p").html(((message.position[0]/Math.PI)*180).toFixed(2));
		$("#output_j2p").html(((message.position[1]/Math.PI)*180).toFixed(2));
		$("#output_j3p").html(((message.position[2]/Math.PI)*180).toFixed(2));
		$("#output_j4p").html(((message.position[3]/Math.PI)*180).toFixed(2));
		$("#output_j5p").html(((message.position[4]/Math.PI)*180).toFixed(2));
		$("#output_j6p").html(((message.position[5]/Math.PI)*180).toFixed(2));
	});
	eef_Sub.subscribe(function(message){
		eef_Sub_lx = message.linear.x;
		eef_Sub_ly = message.linear.y;
		eef_Sub_lz = message.linear.z;
		eef_Sub_ax = message.angular.x;
		eef_Sub_ay = message.angular.y;
		eef_Sub_az = message.angular.z;
		$("#output_lx").html(message.linear.x);
		$("#output_ly").html(message.linear.y);
		$("#output_lz").html(message.linear.z);
		$("#output_ax").html(message.angular.x);
		$("#output_ay").html(message.angular.y);
		$("#output_az").html(message.angular.z);
	});
});
