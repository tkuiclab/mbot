	//EEF_plus or minus
	//cause there has 12 button need to send the value each other,so move this js code stand out the index.js
	$('#plus_lx').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_lx + " + ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx + $('#input_plus_d').val();
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#minus_lx').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_lx + " - ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx - $('#input_plus_d').val();
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#plus_ly').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_ly + " + ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly + $('#input_plus_d').val();
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#minus_ly').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_ly + " - ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly - $('#input_plus_d').val();
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#plus_lz').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_lz + " + ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz + $('#input_plus_d').val();
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#minus_lz').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_lz + " - ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz - $('#input_plus_d').val();
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	//angular
	$('#plus_ax').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_ax + " + ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax + $('#input_plus_d').val();
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#minus_ax').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_ax + " - ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax - $('#input_plus_d').val();
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#plus_ay').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_ay + " + ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay + $('#input_plus_d').val();
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#minus_ay').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_ay + " - ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay - $('#input_plus_d').val();
		float64[5] = eef_Sub_az;
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#plus_az').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_az + " + ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az + $('#input_plus_d').val();
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
	$('#minus_az').on('click',function(e){
		$('#dialog_table_eef').hide();
		$('#dialog_table_joint').hide();
		$('#dialog_table_plus').show();
		$('#dialog_show_plus').html(eef_Sub_az + " - ");
		var float64 = new Float64Array(6);
		float64[0] = eef_Sub_lx;
		float64[1] = eef_Sub_ly;
		float64[2] = eef_Sub_lz;
		float64[3] = eef_Sub_ax;
		float64[4] = eef_Sub_ay;
		float64[5] = eef_Sub_az - $('#input_plus_d').val();
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
		var send_plus = new ROSLIB.Message({
			cmd : 'EEFPosition',
			pose : twist
		});
		mlist.push(send_plus);
		var goal = new ROSLIB.Goal({
			actionClient : teachModeClient,
			goalMessage : {
				cmd_list : mlist
			}
		});
		$("#infoContent").html('Goal was send cmdlist'
					+'<BR>Cmd : ' + send_plus.cmd
					+"<BR>Pose : "
					+"<BR>linear:<BR>"+ send_plus.pose.linear.x +"<BR>"+ send_plus.pose.linear.y +"<BR>"+ send_plus.pose.linear.z
					+"<BR>angular<BR>"+ send_plus.pose.angular.x +"<BR>"+ send_plus.pose.angular.y +"<BR>"+ send_plus.pose.angular.z
		);
		goal.send();
		mlist = [];
	});
