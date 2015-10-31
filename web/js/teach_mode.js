var CmdType = {
	Joint: "Joint",
	PTP: "PTP",
	Line: "Line",
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
}

function get_cmd_id(){
	cmd_id++;
	return cmd_id;
}

$("#cmd_select").change(function() {
	console.log($(this).val());
	cmd = $(this).val();
	if(cmd==CmdType.Joint || cmd==CmdType.PTP || cmd==CmdType.Line){
		hide_all();
		$("#block").show();
		$("#block").css("display","inline");
	}else if(cmd==CmdType.Vaccum){
		hide_all();
		$("#vaccum_block").show();
		$("#vaccum_block").css("display","inline");
	}else{
		hide_all();
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
	
	var teach_a = '<a href="#" class="btn btn-info btn-md teach_btn"><span class="glyphicon glyphicon-pushpin"></span> Teach</a>';
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
	
	//var teach_a = '<a href="#" class="btn btn-info btn-md"><span class="glyphicon glyphicon-search"></span> Teach</a>';
	//teach_a = $(teach_a).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var add_tr = 
	'<tr id="cmd_'+cmd_id_str+'">' +
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

addbtn.onclick = function(){
	console.log("in addBtn");
	var cmd = $("#cmd_select").val();
	var tr_html = '';
	
	if(cmd==CmdType.Joint || cmd==CmdType.PTP || cmd==CmdType.Line){
		tr_html = get_block_tr(cmd);
	}else if(cmd==CmdType.Vaccum){
		tr_html = get_vaccum_tr();
	}

	console.log("tr_html="+tr_html);
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
	var i = 0;
	if(mod==CmdType.Joint || mod==CmdType.PTP || mod==CmdType.Line){
		$('#'+m_cmd_id).children("td.SubCmd").children("input").each(function(){
			//console.log($(this).val());
			$(this).removeAttr("readonly");
			$(this).css("border-style","inset");
			cmd_edit[i++] = $(this).val();
		});
	}else if(mod==CmdType.Vaccum){
		$('#'+m_cmd_id).find('#vaccum_select').removeAttr("disabled");
		$('#'+m_cmd_id).find('#vaccum_select').css("border-style","inset");
		vac_cmd = $('#'+m_cmd_id).find('#vaccum_select').val();
	}else{
	
	}	
}

function save_Cmd(edit){
	var m_cmd_id = $(edit).attr('target_cmd_id');
	console.log("m_cmd_id="+m_cmd_id);
	
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
	console.log("m_cmd_id="+m_cmd_id);
	
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
	console.log("m_cmd_id="+m_cmd_id);
	
	$('#'+m_cmd_id).remove();
}



$("#run_btn").click(function() {
	console.log("in run_btn");
	$(this).removeClass('active');
	$(this).addClass('disabled');
	
	var mlist = [];
	
	
	//get each command
	$('#teach_table tr').each(function() {
		//var cmd_msg;
		var cmd_mod = $('#cmd_mod', this).text();
		console.log(cmd_mod);
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

	console.log('teachModeClient='+teachModeClient);
	
	var goal = new ROSLIB.Goal({
		actionClient : teachModeClient,
		goalMessage : {
			cmd_list : mlist
		}
	});
	goal.on('feedback', teach_feedback);
	goal.on('result', teach_result);
	goal.send();
});

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

function teach_feedback(feedback){
	
	console.log('Feedback: ' + feedback.status);
}

function teach_result(result){
	
	console.log('Final Result: ' + result.notify);
	$("#run_btn").removeClass('disabled');
	$("#run_btn").addClass('active');
}





