var CmdType = {
	Joint: "Joint",
	PTP: "PTP",
	Line: "Line",
	Shift_X: "Shift_X",
	Shift_Y: "Shift_Y",
	Shift_Z: "Shift_Z",
	Vaccum: "Vaccum"
};

var addbtn = document.getElementById("addbtn");
var edit_img = '<img id="edit_btn" src="img/edit.png" onclick="edit_Cmd(this)"/>';
var cmd_id = 0;


//deg.pad(4) // "0045"
Number.prototype.pad = function(n) {
    return new Array(n).join('0').slice((n || 2) * -1) + this;
}
	
function hide_all(){
	$("#block").hide();
	$("#vaccum_block").hide();
	$("#shift_block").hide();
}

function get_cmd_id(){
	cmd_id++;
	return cmd_id;
}

$("#cmd_select").change(function() {
	console.log($(this).val());
	cmd = $(this).val();
	
	hide_all();
	if(cmd==CmdType.Joint || cmd==CmdType.PTP || cmd==CmdType.Line){
		//hide_all();
		$("#block").show();
		$("#block").css("display","inline");
	}else if(cmd==CmdType.Vaccum){
		//hide_all();
		$("#vaccum_block").show();
		$("#vaccum_block").css("display","inline");
	}else if(cmd==CmdType.Shift_X || cmd==CmdType.Shift_Y ||cmd==CmdType.Shift_Z){
		//hide_all();
		$("#shift_block").show();
		$("#shift_block").css("display","inline");
	}
});



function get_block_tr(option){
	var sub_cmd = '';
	var cmd_id = get_cmd_id();
	var cmd_id_str = 'cmd_' + cmd_id;
	for(var i=1;i<=6;i++){
		var t_id = '#block_'+i;
		sub_cmd += '<input style="width: 15%; border-style:none;" type="number" value="'+$(t_id).val()+'"readonly>';
	}
	
	var edit_img_new = $(edit_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var true_img = '<img id="true_btn" src="img/true.png" class="img_show" onclick="save_Cmd(this)"/>';
	true_img = $(true_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');

	var false_img = '<img id="false_btn" src="img/false.png" class="img_show" onclick="break_Cmd(this)"/>';
	false_img = $(false_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var delete_img = '<img id="delete_opt" src="img/delete.png" style="width:20%; height:auto;" onclick="delete_Cmd(this)"/>';			
	delete_img = $(delete_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var teach_a = '<a id="teach_btn" href="#" class="btn btn-info btn-block" onclick="teach_click(this)"><span class="glyphicon glyphicon-pushpin"></span> Teach</a>';
	teach_a = $(teach_a).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	
	var add_tr = 
	'<tr id='+cmd_id_str+'>' +
		'<td>'+cmd_id.pad(3)+'</td>'+
		'<td id="cmd_mod">'+CmdType[option]+'</td>'+
		'<td class="SubCmd">'+sub_cmd+'</td>'+
		'<td>'+edit_img_new+
		true_img +
		false_img +
		'</td>'+
		'<td>'+delete_img+'</td>'+
		'<td>'+teach_a +'</td>'+
	'</tr>';
	
	return add_tr;
}

function get_vaccum_tr(){
	
	var cmd_id = get_cmd_id();
	var cmd_id_str = 'cmd_' + cmd_id;
	var sub_cmd = $('#vaccum_select').val();
	
	if(sub_cmd == "On"){
		var sub_cmd_edit =
		'<select class="options" id="vaccum_select" disabled="disabled" style="border-style: none">' +
			'<option value="On" selected>On</option>'+
			'<option value="Off">Off</option>' +
		'</select>';
	}else if(sub_cmd == "Off"){
		var sub_cmd_edit =
		'<select class="options" id="vaccum_select" disabled="disabled" style="border-style: none">' +
			'<option value="On">On</option>'+
			'<option value="Off" selected>Off</option>' +
		'</select>';
	}
	
	var edit_img_new = $(edit_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var true_img = '<img id="true_btn" src="img/true.png" class="img_show" onclick="save_Cmd(this)"/>';
	true_img = $(true_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var false_img = '<img id="false_btn" src="img/false.png" class="img_show" onclick="break_Cmd(this)"/>';
	false_img = $(false_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var delete_img = '<img id="delete_opt" src="img/delete.png" style="width:20%; height:auto;" onclick="delete_Cmd(this)"/>';
	delete_img = $(delete_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	
	var add_tr = 
	'<tr id="'+cmd_id_str+'">' +
		'<td>'+cmd_id.pad(3)+'</td>'+
		'<td id="cmd_mod">'+CmdType.Vaccum+'</td>'+
		'<td id="edit">'+sub_cmd_edit+'</td>'+
		'<td>'+edit_img_new+
		true_img +
		false_img +
		'</td>'+
		'<td>'+delete_img+'</td>'+
		'<td>'+'' +'</td>'+
	'</tr>';
	
	return add_tr;
}


function get_shift_tr(option){
	var sub_cmd = '';
	var cmd_id = get_cmd_id();
	var cmd_id_str = 'cmd_' + cmd_id;
	// for(var i=1;i<=6;i++){
		// var t_id = '#block_'+i;
		// sub_cmd += '<input style="width: 15%; border-style:none;" type="number" value="'+$(t_id).val()+'"readonly>';
	// }
	sub_cmd += '<input style="width: 15%; border-style:none;" type="number" value="'+$('#shift_val').val()+'"readonly>';
	console.log('option='+option);
	
	var edit_img_new = $(edit_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var true_img = '<img id="true_btn" src="img/true.png" class="img_show" onclick="save_Cmd(this)"/>';
	true_img = $(true_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');

	var false_img = '<img id="false_btn" src="img/false.png" class="img_show" onclick="break_Cmd(this)"/>';
	false_img = $(false_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var delete_img = '<img id="delete_opt" src="img/delete.png" style="width:20%; height:auto;" onclick="delete_Cmd(this)"/>';			
	delete_img = $(delete_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var teach_a = '<a id="teach_btn" href="#" class="btn btn-info btn-block" onclick="teach_click(this)"><span class="glyphicon glyphicon-pushpin"></span> Teach</a>';
	teach_a = $(teach_a).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	
	var add_tr = 
	'<tr id='+cmd_id_str+'>' +
		'<td>'+cmd_id.pad(3)+'</td>'+
		'<td id="cmd_mod">'+CmdType[option]+'</td>'+
		'<td class="SubCmd">'+sub_cmd+'</td>'+
		'<td>'+edit_img_new+
		true_img +
		false_img +
		'</td>'+
		'<td>'+delete_img+'</td>'+
		'<td>'+teach_a +'</td>'+
	'</tr>';
	
	return add_tr;
}

addbtn.onclick = function(){
	//console.log("in addBtn");
	var cmd = $("#cmd_select").val();
	var tr_html = '';
	
	if(cmd==CmdType.Joint || cmd==CmdType.PTP || cmd==CmdType.Line){
		tr_html = get_block_tr(cmd);
	}else if(cmd==CmdType.Vaccum){
		tr_html = get_vaccum_tr(cmd);
	}else if(cmd==CmdType.Shift_X || cmd==CmdType.Shift_Y || cmd==CmdType.Shift_Z){
		tr_html = get_shift_tr(cmd);
	}

	//console.log("tr_html="+tr_html);
	$('#teach_table').append(tr_html);
	
}

var cmd_edit = new Array;
var vac_cmd;

function edit_Cmd(edit){
	var m_cmd_id = $(edit).attr('target_cmd_id');
	console.log("m_cmd_id="+m_cmd_id);
	
	$('#'+m_cmd_id).find('#edit_btn').hide();
	$('#'+m_cmd_id).find('#true_btn').show();
	$('#'+m_cmd_id).find('#false_btn').show();
	
	var mod = $('#'+m_cmd_id).children("#cmd_mod").text();
	//console.log("mod="+mod);
	
	var i = 0;
	if(mod==CmdType.Joint || mod==CmdType.PTP || mod==CmdType.Line){
		$('#'+m_cmd_id).children("td.SubCmd").children("input").each(function(){
			//console.log($(this).val());
			$(this).removeAttr("readonly");
			$(this).css("border-style","inset");
			cmd_edit[i++] = $(this).val();
		});
	}else if(mod==CmdType.Shift_X || mod==CmdType.Shift_Y || mod==CmdType.Shift_Z){
		var t_input = $('#'+m_cmd_id).children("td.SubCmd").children("input");
		
		//console.log($(this).val());
		t_input.removeAttr("readonly");
		t_input.css("border-style","inset");
		cmd_edit[i++] = $(this).val();
	
	}else if(mod==CmdType.Vaccum){
		$('#'+m_cmd_id).find('#vaccum_select').removeAttr("disabled");
		$('#'+m_cmd_id).find('#vaccum_select').css("border-style","inset");
		vac_cmd = $('#'+m_cmd_id).find('#vaccum_select').val();
	}else{
	
	}	
}

function save_Cmd(edit){
	var m_cmd_id = $(edit).attr('target_cmd_id');
	//console.log("m_cmd_id="+m_cmd_id);
	
	$('#'+m_cmd_id).find('#edit_btn').show();
	$('#'+m_cmd_id).find('#true_btn').hide();
	$('#'+m_cmd_id).find('#false_btn').hide();
	
	var mod = $('#'+m_cmd_id).children("#cmd_mod").html();
	
	if(mod==CmdType.Joint || mod==CmdType.PTP || mod==CmdType.Line){
		$('#'+m_cmd_id).children("td.SubCmd").children("input").each(function(){
			$(this).attr("readonly");
			$(this).css("border-style","none");
		});
	}else if(mod==CmdType.Vaccum){
		$('#'+m_cmd_id).find('#vaccum_select').attr("disabled","disabled");
		$('#'+m_cmd_id).find('#vaccum_select').css("border-style","none");
	}else{
	
	}
}

function break_Cmd(edit){
	var m_cmd_id = $(edit).attr('target_cmd_id');
	//console.log("m_cmd_id="+m_cmd_id);
	
	$('#'+m_cmd_id).find('#edit_btn').show();
	$('#'+m_cmd_id).find('#true_btn').hide();
	$('#'+m_cmd_id).find('#false_btn').hide();
	
	var mod = $('#'+m_cmd_id).children("#cmd_mod").html();
	var i = 0;
	if(mod==CmdType.Joint || mod==CmdType.PTP || mod==CmdType.Line){
		$('#'+m_cmd_id).children("td.SubCmd").children("input").each(function(){
			$(this).val(cmd_edit[i++]);
			$(this).attr("readonly");
			$(this).css("border-style","none");
		});
	}else if(mod==CmdType.Vaccum){
		$('#'+m_cmd_id).find('#vaccum_select').val(vac_cmd);
		$('#'+m_cmd_id).find('#vaccum_select').attr("disabled","disabled");
		$('#'+m_cmd_id).find('#vaccum_select').css("border-style","none");
	}else{
	
	}
}

function delete_Cmd(edit){
	var m_cmd_id = $(edit).attr('target_cmd_id');
	//console.log("m_cmd_id="+m_cmd_id);
	
	$('#'+m_cmd_id).remove();
}

function get_twist(){
	var twist = new ROSLIB.Message({
		linear : {
			x : 0.0,
			y : 0.0,
			z : 0.0,
		},
		angular : {
			x : 0.0,
			y : 0.0,
			z : 0.0,
		}
		}
	);
	
	return twist;
}

$("#run_btn").click(function() {
	//console.log("in run_btn");
	$(this).removeClass('active');
	$(this).addClass('disabled');
	
	var mlist = [];
	
	
	//get each command
	$('#teach_table tr').each(function() {
		//var cmd_msg;
		var cmd_mod = $('#cmd_mod', this).text();
		//console.log(cmd_mod);
		//-------------CmdType.Joint-------------//
		if(cmd_mod==CmdType.Joint){
			var float_ary = [];
			 $('input', this).each(function()
		    {
		    	var t_float = parseFloat( $(this).val() );
		    	//console.log('$(this).val()='+t_float);
		        float_ary.push( t_float );
		    });
			
			
			var cmd_msg = new ROSLIB.Message({
				cmd : CmdType.Joint,
				joint_position : float_ary
			});
			mlist.push(cmd_msg);
		//-------------CmdType.PTP-------------//
		}else if(cmd_mod==CmdType.PTP){
		    
			var refer = $(this).children("td.SubCmd");
			var twist = new ROSLIB.Message({
				linear : {
					x : parseFloat(refer.children("input:nth-child(1)").val()),
					y : parseFloat(refer.children("input:nth-child(2)").val()),
					z : parseFloat(refer.children("input:nth-child(3)").val()),
				},
				angular : {
					x : parseFloat(refer.children("input:nth-child(4)").val()),
					y : parseFloat(refer.children("input:nth-child(5)").val()),
					z : parseFloat(refer.children("input:nth-child(6)").val()),
				}
				}
			);
			console.log('twist.linear.x ='+ twist.linear.x  +',y=' + twist.linear.y + ',z=' + twist.linear.z);
		
			
			
			var cmd_msg = new ROSLIB.Message({
				cmd : CmdType.PTP,
				pose : twist
			});
			mlist.push(cmd_msg);
		//-------------CmdType.Shift_X-------------//
		}else if(cmd_mod==CmdType.Shift_X || cmd_mod==CmdType.Shift_Y || cmd_mod==CmdType.Shift_Z){
		    
			var data = $(this).children("td.SubCmd").children("input:first").val();
			var twist = get_twist();
			
			if(cmd_mod==CmdType.Shift_X){
				twist.linear.x = parseFloat(data);
			}else if(cmd_mod==CmdType.Shift_Y){
				twist.linear.y = parseFloat(data);
			}else if(cmd_mod==CmdType.Shift_Z){
				twist.linear.z = parseFloat(data);
			}
			//console.log('twist.linear.x ='+ twist.linear.x  +',y=' + twist.linear.y + ',z=' + twist.linear.z);
			
			var cmd_msg = new ROSLIB.Message({
				cmd : cmd_mod,
				pose : twist
			});
			mlist.push(cmd_msg);
		//-------------CmdType.Vaccum-------------//
		}else if(cmd_mod==CmdType.Vaccum){
			var vaccum_yn = $('#vaccum_select', this).val()=='On' ? true:false;
			
			
			var cmd_msg = new ROSLIB.Message({
				cmd : CmdType.Vaccum,
				vaccum : vaccum_yn
			});
			
			mlist.push(cmd_msg);
		}else{
			
		}
		
		
	});

	//console.log('teachModeClient='+teachModeClient);
	
	var goal = new ROSLIB.Goal({
		actionClient : teachModeClient,
		goalMessage : {
			cmd_list : mlist
		}
	});
	goal.on('feedback', teach_feedback);
	goal.on('result', teach_result);
	
	
	teach_result_trigger = false;
	now_exe_id = 0;
	
	goal.send();
});


/* json example
{
  "Joint":{
    "Val_6": [0,0.3,0.4,0,1.57,0]
  },
  "PTP":{
    "Val_6": [0,0.3,0.4,0,1.57,0]
  },
  "Shift_Y":{
    "Val": 0.2
  }
  
}
 */
$("#file_save_btn").click(function() {
	var save_data = "{\n";
	$('#teach_table tr').each(function() {
		//var cmd_msg;
		var cmd_mod = $('#cmd_mod', this).text();
		//console.log(cmd_mod);
		//-------------CmdType.Joint-------------//
		if(cmd_mod==CmdType.Joint || cmd_mod==CmdType.PTP || cmd_mod==CmdType.Line){
			save_data += '\t"'+cmd_mod+'":{\n';	// Joint or PTP or Line START
			save_data += '\t\t"Val_6": ';	  //Val_6 Start
			var float_ary = [];
			 $('input', this).each(function()
		    {
		    	var t_float = parseFloat( $(this).val() );
		        float_ary.push( t_float );
		    });
			save_data += '[' + float_ary.toString()+"]\n";  //Val_6 End
			
			save_data += '\t},\n'; // Joint or PTP or Line  END
		//-------------CmdType.PTP-------------//
		}else if(cmd_mod==CmdType.Shift_X || cmd_mod==CmdType.Shift_Y || cmd_mod==CmdType.Shift_Z){
			save_data += '\t"'+cmd_mod+'":{\n';	// Shift_X or Shift_Y or Shift_Z START
			save_data += '\t\t"Val": ';	  //Val Start
			var Vaccum = $(this).children("td.SubCmd").children("input:first").val();
			save_data += '[' + val +"]\n";  //Val End
			
			save_data += '\t},\n'; // Shift_X or Shift_Y or Shift_Z  END
		}else if(cmd_mod==CmdType.Vaccum){
			save_data += '\t"'+cmd_mod+'":{\n';	// Vaccum START
			save_data += '\t\t"Val": ';	  //Val Start
			var vaccum_yn = $('#vaccum_select', this).val()=='On' ? true:false;
			save_data += '[' + vaccum_yn +"]\n";  //Val End
			
			save_data += '\t},\n'; // Vaccum END
		}
	});
	
  
	
	save_data += "}";
	
	$("#test_json_data").val(save_data);
	
});	


function teach_click(t){
	//console.log('in teach btn');
	
	var m_cmd_id = $(t).attr('target_cmd_id');
	console.log("m_cmd_id="+m_cmd_id);
	
	var mod = $('#'+m_cmd_id).children("#cmd_mod").text();
	//console.log("mod="+mod);
	
	var i = 0;
	if(mod==CmdType.Joint){
		var i = 0;
		$('#'+m_cmd_id).children("td.SubCmd").children("input").each(function(){
			//$(this).val(joint_ary[i++].toFixed(5));			//toFixed ex:  0.123456789  ->  0.1234
			$(this).val(joint_ary[i++]);			//ex:  0.123456789  ->  0.1234
		});
	}else if(mod==CmdType.PTP || mod==CmdType.Line){
		var request = new ROSLIB.ServiceRequest({
		    cmd : "Teach:EEF_Pose",
		});
		
		ui_client.callService(request, function(res) {
			var l = res.pose.linear;
			var a = res.pose.angular;
			
			console.log( 'Result : '   + res.result);
			console.log( 'Pose : '   + l.x + "," + l.y + "," + l.z + "," + a.x + "," + a.y + "," + a.z );
		  	
		  	
		  	var refer = $('#'+m_cmd_id).children("td.SubCmd");
		  	refer.children("input:nth-child(1)").val(l.x.toFixed(2));
		  	refer.children("input:nth-child(2)").val(l.y.toFixed(2));
		  	refer.children("input:nth-child(3)").val(l.z.toFixed(2));
		  	refer.children("input:nth-child(4)").val(a.x.toFixed(2));
		  	refer.children("input:nth-child(5)").val(a.y.toFixed(2));
		  	refer.children("input:nth-child(6)").val(a.z.toFixed(2));
		  	
		  	
		});
	
	}else if(mod==CmdType.Shift_X || mod==CmdType.Shift_Y || mod==CmdType.Shift_Z){
		
		var find = false;
		
		var now_cmd_id = m_cmd_id;
		var request;
		do{
			
			
			//get my tag name
			//var now_tag_name = $('#'+now_cmd_id).prop('tagName').toLowerCase();
			//get previous tr's id
			var pre_id = $('#'+now_cmd_id).prev("tr").prop("id");
			
			if(pre_id==undefined)	{
				console.error('Teach Click -> Cannot find previous position');
				return;
			}
			
			//get previous tr's command
			var pre_mod = $('#'+pre_id).children("#cmd_mod").text();
			
			
			//console.log('pre_id='+pre_id+',pre_mod='+pre_mod);
			
			if(pre_mod==CmdType.Joint){
				var float_ary = [];
				 $('#'+pre_id).children("td.SubCmd").children("input").each(function()
			    {
			    	var t_float = parseFloat( $(this).val() );
			        float_ary.push( t_float );
			    });
			 	request = new ROSLIB.ServiceRequest({
				    cmd : "Teach:" + mod,
				    float_ary : float_ary
				});
				
				find = true;
				
			}else if(pre_mod==CmdType.PTP || pre_mod==CmdType.Line){
				var refer = $('#'+pre_id).children("td.SubCmd");
				var twist = new ROSLIB.Message({
				    linear : {
				      x : parseFloat(refer.children("input:nth-child(1)").val()),
				      y : parseFloat(refer.children("input:nth-child(2)").val()),
				      z : parseFloat(refer.children("input:nth-child(3)").val()),
				    },
				    angular : {
				      x : parseFloat(refer.children("input:nth-child(4)").val()),
				      y : parseFloat(refer.children("input:nth-child(5)").val()),
				      z : parseFloat(refer.children("input:nth-child(6)").val()),
				    }
				});
				console.log('twist.linear.x ='+ twist.linear.x  +',y=' + twist.linear.y + ',z=' + twist.linear.z);
				
				request = new ROSLIB.ServiceRequest({
				    cmd : "Teach:" + mod,
				    pose : twist
				});
				
				find = true;
			}else if(pre_mod==CmdType.Shift_X || pre_mod==CmdType.Shift_Y || pre_mod==CmdType.Shift_Z){
				
			}
			
			now_cmd_id = pre_id;
			
		}while(!find);
		
	
		if(!find)	return;
		
		//client call service
		ui_client.callService(request, function(res) {
			
	  		var shift = res.f;
	  		$('#'+m_cmd_id).children("td.SubCmd").children("input").val(shift.toFixed(2));;

		});
	} 
	
	
}

//----------------------------------------ROS----------------------------------------//
// Connecting to ROS
var ros = new ROSLIB.Ros({
	url : 'ws://localhost:9090'
});

// If there is an error on the backend, an 'error' emit will be emitted.
ros.on('error', function(error) {
	console.log(error);
});

// Find out exactly when we made a connection.
ros.on('connection', function() {
	console.log('ROS Connection made!');
});

ros.on('close', function() {
    console.log('ROS Connection closed.');
});

//-----------ActionClient-------------//
var teachModeClient = new ROSLIB.ActionClient({
	ros : ros,
	serverName : '/teach_mode_server',
	actionName : 'mbot_control/TeachCommandListAction'
});


var now_exe_id = 0;
var teach_result_trigger = false;

function teach_feedback(feedback){
	if(teach_result_trigger)	return;
	console.log('Feedback: ' + feedback.status);
	
	var arrow_img = '<img src="img/right_arrow.png" align="center" style="width: 35%;"/>';
	
	//get cmd_id
	var fb_str = feedback.status;
	var str_index = fb_str.indexOf('->');
	var exe_id = fb_str.substring(str_index+2,fb_str.length);
	var m_cmd_id = 'cmd_'+exe_id;
	console.log('m_cmd_id=' + m_cmd_id);
	//change to arrow_img
	$('#'+m_cmd_id).children("td:first").html(arrow_img);
	
	
	if(now_exe_id!=0){
		m_cmd_id = 'cmd_'+now_exe_id;
		//change to number
		$('#'+m_cmd_id).children("td:first").html(now_exe_id.pad(3));	
	}
	
	now_exe_id = parseInt(exe_id);
}

function teach_result(result){
	
	console.log('Final Result: ' + result.notify);
	$("#run_btn").removeClass('disabled');
	$("#run_btn").addClass('active');
	
	
	/*
	$('#teach_table tr').each(function() {
		$(this).children("td:first").html(now_exe_id.pad(3));	
	});*/
	
	
	teach_result_trigger = true;
	
	
	if(now_exe_id!=0){
		m_cmd_id = 'cmd_'+now_exe_id;
		//change to number
		$('#'+m_cmd_id).children("td:first").html(now_exe_id.pad(3));	
	}
	
	
}


// ------------------------------------//
// Subscribing to a "joint_states" Topic
// -----------------------------------//

var joint_ary = new Float32Array(6);;

var joint_sub = new ROSLIB.Topic({
	ros:ros,
	name: '/joint_states',
	messageType : 'sensor_msgs/JointState'
});


joint_sub.subscribe(function(msg){
	for(var i =0 ;i < 6;i++){
		joint_ary[i] = msg.position[i];
	}
});	



// ------------------------------------//
// Client for a "ui_server" Service
// -----------------------------------//


var ui_client = new ROSLIB.Service({
    ros : ros,
    name : '/ui_server',
    serviceType : 'mbot_control/UI_Server'
  });

