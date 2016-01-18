var CmdType = {
	Joint: "Joint",
	PTP: "PTP",
	Line: "Line",
	Shift_X: "Shift_X",
	Shift_Y: "Shift_Y",
	Shift_Z: "Shift_Z",
	Shift_RX: "Shift_RX",
	Shift_RY: "Shift_RY",
	Shift_RZ: "Shift_RZ",
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
	}else if(cmd==CmdType.Shift_X || cmd==CmdType.Shift_Y ||cmd==CmdType.Shift_Z || 
		     cmd==CmdType.Shift_RX || cmd==CmdType.Shift_RY ||cmd==CmdType.Shift_RZ ){
		//hide_all();
		$("#shift_block").show();
		$("#shift_block").css("display","inline");
	}
});



function get_block_tr(option,val_6){
	var sub_cmd = '';
	var cmd_id = get_cmd_id();
	var cmd_id_str = 'cmd_' + cmd_id;
	if(val_6==undefined){
		for(var i=1;i<=6;i++){
			var t_id = '#block_'+i;
			sub_cmd += '<input style="width: 15%; border-style:none;" type="number" value="'+$(t_id).val()+'"readonly>\n';
		}
	}else{
		for(var i=0;i<6;i++){
			sub_cmd += '<input style="width: 15%; border-style:none;" type="number" value="'+val_6[i]+'"readonly>\n';
		}
		
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

function get_vaccum_tr(val){
	
	var cmd_id = get_cmd_id();
	var cmd_id_str = 'cmd_' + cmd_id;
	
	
	var on_selected = '';
	var off_selected = '';
	if(val==undefined){
		var sub_cmd = $('#vaccum_select').val();
	
		on_selected =  (sub_cmd == "On") ? "selected" : "";
		off_selected = (sub_cmd == "Off") ? "selected" : "";
	}else{
		on_selected =  (val == true) ? "selected" : "";
		off_selected = (val == false) ? "selected" : "";
	}
	
	var sub_cmd_edit =
		'<select class="options" id="vaccum_select" disabled="disabled" style="border-style: none">' +
			'<option value="On" ' + on_selected +'>On</option>'+
			'<option value="Off" '+ off_selected +'>Off</option>' +
		'</select>';
		
	
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


function get_shift_tr(option,val,pose){
	
	var cmd_id = get_cmd_id();
	var cmd_id_str = 'cmd_' + cmd_id;
	
	
	var input_val = (val==undefined) ? $('#shift_val').val():val;
	
	var sub_cmd = '';
	sub_cmd += '<input style="width: 15%; border-style:none;" type="number" value="'+input_val+'"readonly>';
	if(pose!=undefined){
		sub_cmd = $(sub_cmd).attr('pose',pose).prop('outerHTML');
	}
	//console.log('option='+option);
	
	var edit_img_new = $(edit_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var true_img = '<img id="true_btn" src="img/true.png" class="img_show" onclick="save_Cmd(this)"/>';
	true_img = $(true_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');

	var false_img = '<img id="false_btn" src="img/false.png" class="img_show" onclick="break_Cmd(this)"/>';
	false_img = $(false_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	var delete_img = '<img id="delete_opt" src="img/delete.png" style="width:20%; height:auto;" onclick="delete_Cmd(this)"/>';			
	delete_img = $(delete_img).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	
	
	var teach_a = '';
	if(option==CmdType.Shift_X  || option==CmdType.Shift_Y  || option==CmdType.Shift_Z ){
		teach_a = '<a id="teach_btn" href="#" class="btn btn-info btn-block" onclick="teach_click(this)"><span class="glyphicon glyphicon-pushpin"></span> Teach</a>';
		teach_a = $(teach_a).attr('target_cmd_id', cmd_id_str).prop('outerHTML');
	}
	
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
	}else if(cmd==CmdType.Shift_X  || cmd==CmdType.Shift_Y  || cmd==CmdType.Shift_Z ||
			 cmd==CmdType.Shift_RX || cmd==CmdType.Shift_RY || cmd==CmdType.Shift_RZ ){
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
	}else if(mod==CmdType.Shift_X  || mod==CmdType.Shift_Y || mod==CmdType.Shift_Z ||
			 mod==CmdType.Shift_RX || mod==CmdType.Shift_RY || mod==CmdType.Shift_RZ ){
		
		
		 
		var t_input = $('#'+m_cmd_id).children("td.SubCmd").children("input");
		t_input.removeAttr("readonly");
		t_input.css("border-style","inset");
		
		//cmd_edit[i++] = $(this).val();
		cmd_edit[i++] = t_input.val();

	
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
		var m_tag = $('#'+m_cmd_id).children("td.SubCmd").children("input");
		m_tag.attr("readonly");
		m_tag.css("border-style","none");
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
		//}else if(cmd_mod==CmdType.PTP){
		}else if(cmd_mod==CmdType.PTP || cmd_mod==CmdType.Line){
		    
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
				cmd : cmd_mod,
				pose : twist
			});
			mlist.push(cmd_msg);
		//-------------CmdType.Shift_X-------------//
		}else if(cmd_mod==CmdType.Shift_X  || cmd_mod==CmdType.Shift_Y  || cmd_mod==CmdType.Shift_Z||
			     cmd_mod==CmdType.Shift_RX || cmd_mod==CmdType.Shift_RY || cmd_mod==CmdType.Shift_RZ ){
		    
			var data = $(this).children("td.SubCmd").children("input:first").val();
			var twist = get_twist();
			
			if(cmd_mod==CmdType.Shift_X){
				twist.linear.x = parseFloat(data);
			}else if(cmd_mod==CmdType.Shift_Y){
				twist.linear.y = parseFloat(data);
			}else if(cmd_mod==CmdType.Shift_Z){
				twist.linear.z = parseFloat(data);
			}else if(cmd_mod==CmdType.Shift_RX){
				twist.angular.x = parseFloat(data);
			}else if(cmd_mod==CmdType.Shift_RY){
				twist.angular.y = parseFloat(data);
			}else if(cmd_mod==CmdType.Shift_RZ){
				twist.angular.z = parseFloat(data);
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


/* ------json example------
{
	"001":{
		"cmd": "PTP",
		"val_6": [-0.2,0.3,0.7,0,-1.57,0]
	},
	"002":{
		"cmd": "Shift_Y",
		"val": 0.3
	},
	"003":{
		"cmd": "Shift_Z",
		"val": -0.2
	},
	"004":{
		"cmd": "Vaccum",
		"val": true
	},
	"005":{
		"cmd": "Shift_Z",
		"val": 0.2
	}
  
}
 */
$("#file_save_btn").click(function() {
	$(this).removeClass('active');
	$(this).addClass('disabled');
	
	var save_data = "{\n";
	
	var cmd_count = $('#teach_table tr').length;
	$('#teach_table tr').each(function(index,element) {
		//var cmd_msg;
		var cmd_mod = $('#cmd_mod', this).text();
		//console.log(cmd_mod);
		//-------------CmdType.Joint-------------//
		save_data += '\t"'+$(this).children('td:first').html()+'":{\n';	
		if(cmd_mod==CmdType.Joint || cmd_mod==CmdType.PTP || cmd_mod==CmdType.Line){
			save_data += '\t\t"cmd": "'+cmd_mod+'",\n';	// Joint or PTP or Line START
			save_data += '\t\t"val_6": ';	  //val_6 Start
			var float_ary = [];
			 $('input', this).each(function()
		    {
		    	var t_float = parseFloat( $(this).val() );
		        float_ary.push( t_float );
		    });
			save_data += '[' + float_ary.toString()+"]\n";  //val_6 End
			
			//save_data += '\t},\n'; // Joint or PTP or Line  END
		//-------------CmdType.PTP-------------//
		}else if(cmd_mod==CmdType.Shift_X  || cmd_mod==CmdType.Shift_Y  || cmd_mod==CmdType.Shift_Z ||
			     cmd_mod==CmdType.Shift_RX || cmd_mod==CmdType.Shift_RY || cmd_mod==CmdType.Shift_RZ ){
			//save_data += '\t"'+cmd_mod+'":{\n';	// Shift_X or Shift_Y or Shift_Z START
			save_data += '\t\t"cmd": "'+cmd_mod+'",\n';	// Joint or PTP or Line START
			save_data += '\t\t"val": ';	  //Val Start
			
			var refer = $(this).children("td.SubCmd").children("input:first");
			var val = refer.val();
			save_data +=  val ;  //Val End
			
			//console.log('refer.prop("pose")='+refer.attr('pose'));
			
			if(refer.attr('pose')!=undefined){
				save_data +=  ',\n';
				save_data += '\t\t"pose": ' + '[' + refer.attr('pose') +"]\n";	  //pose
				
			}
			
			save_data +=  '\n';
			
			//save_data += '\t},\n'; // Shift_X or Shift_Y or Shift_Z  END
		}else if(cmd_mod==CmdType.Vaccum){
			//save_data += '\t"'+cmd_mod+'":{\n';	// Vaccum START
			save_data += '\t\t"cmd": "'+cmd_mod+'",\n';	// Joint or PTP or Line START
			save_data += '\t\t"val": ';	  //Val Start
			var vaccum_yn = $('#vaccum_select', this).val()=='On' ? true:false;
			save_data +=  vaccum_yn +"\n";  //Val End
			
			//save_data += '\t},\n'; // Vaccum END
		}
		
		if(index==cmd_count-1){
			save_data += '\t}\n'; 
		}else{
			save_data += '\t},\n'; 
		}
		
	});
	save_data += "}";
	var request = new ROSLIB.ServiceRequest({
	    cmd : "Teach:SaveFile",
	    req_s : save_data
	});
	
	ui_client.callService(request, function(res) {
		console.log( 'Result : '   + res.result);
	  	$("#file_save_btn").removeClass('disabled');
		$("#file_save_btn").addClass('active');
	});
	
  
	$("#test_json_data").val(save_data);
	
});	




$("#file_read_btn").click(function() {
	$(this).removeClass('active');
	$(this).addClass('disabled');
	
	var request = new ROSLIB.ServiceRequest({
	    cmd : "Teach:ReadFile"
	});
	
	ui_client.callService(request, function(res) {
		console.log('Result : '   + res.result);
		cmd_id = 0;
		
		$('#teach_table').html('');
		
		
		$("#test_json_data").val(res.res_s);
		
		var json = JSON.parse(res.res_s);     
		
		
		for (var index in json) {
			var cmd = json[index].cmd;
			//console.log('cmd : ' + cmd);
			
			
			var tr_html = '';
			if(cmd==CmdType.PTP || cmd==CmdType.Line){
				tr_html = get_block_tr(cmd,json[index].val_6);
				
			}else if(cmd==CmdType.Vaccum){
				tr_html = get_vaccum_tr(json[index].val);
			}else if(cmd==CmdType.Shift_X  || cmd==CmdType.Shift_Y  || cmd==CmdType.Shift_Z||
			     	 cmd==CmdType.Shift_RX || cmd==CmdType.Shift_RY || cmd==CmdType.Shift_RZ ){
				tr_html = get_shift_tr(cmd,json[index].val,json[index].pose);
				
		
				
				
			}
			
			
			$('#teach_table').append(tr_html);

		}
		
		
	  	$("#file_read_btn").removeClass('disabled');
		$("#file_read_btn").addClass('active');
	});

});	


function parse_json_2_cmd_list(cmd,val){
	var tr_html = '';
	
	
	console.log('cmd='+cmd+',val='+val)
	
	if(cmd==CmdType.PTP || cmd==CmdType.Line){
		tr_html = get_block_tr(cmd,val.val_6);
		
	}else if(cmd==CmdType.Vaccum){
		tr_html = get_vaccum_tr(val.Val);
	}else if(cmd==CmdType.Shift_X  || cmd==CmdType.Shift_Y  || cmd==CmdType.Shift_Z ||
			 cmd==CmdType.Shift_RX || cmd==CmdType.Shift_RY || cmd==CmdType.Shift_RZ ){
		tr_html = get_shift_tr(cmd,val.Val);
	}else{
		
		return;
	}
	
	
	$('#teach_table').append(tr_html);
	
	
}

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
		var pre_pose = [];
		
		
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
			
			/*
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
							
						}else */
			// 
			if(pre_mod==CmdType.PTP || pre_mod==CmdType.Line){
				var refer = $('#'+pre_id).children("td.SubCmd");
				

				refer.children('input').each(function()
			    {
			    	var t_float = parseFloat( $(this).val() );
			    	
			        pre_pose.push( t_float );
			    });
			
			
				find = true;
			}else if(pre_mod==CmdType.Shift_X || pre_mod==CmdType.Shift_Y || pre_mod==CmdType.Shift_Z){
				
				var pre_pose_str =  $('#'+pre_id).children("td.SubCmd").children("input").attr('pose');
				console.log('pre_pose_str='+pre_pose_str);
				
				if(pre_pose_str!=undefined){
					console.log('in pre_pose_str!=undefined');
					var pre_pose_ary = pre_pose_str.split(",");
					for(var ind in pre_pose_ary){
						console.log('str='+pre_pose_ary[ind]);
						pre_pose.push( parseFloat( pre_pose_ary[ind] ) );
					}

					find = true;
				}
			}
				
			now_cmd_id = pre_id;
			
		}while(!find);
		
	
		if(!find)	return;
			
			
		var twist = new ROSLIB.Message({
		    linear : {
		      x : pre_pose[0],
		      y : pre_pose[1],
		      z : pre_pose[2]
		    },
		    angular : {
		      x : pre_pose[3],
		      y : pre_pose[4],
		      z : pre_pose[5]
		    }
		});
		console.log('twist.linear.x ='+ twist.linear.x  +',y=' + twist.linear.y + ',z=' + twist.linear.z);
		
		request = new ROSLIB.ServiceRequest({
		    cmd : "Teach:" + mod,
		    pose : twist
		});
			
		
		
		//client call service
		ui_client.callService(request, function(res) {
			
	  		var shift = res.f.toFixed(3);
	  		$('#'+m_cmd_id).children("td.SubCmd").children("input").val(shift);;
	  		
	  		var now_pose = pre_pose;
	  		
	  		//console.log('mod =' + mod+',now_pose='+now_pose.toString() );
	  		
	  		
	  		if     (mod==CmdType.Shift_X){  	now_pose[0] += parseFloat(shift);		now_pose[0] = now_pose[0].toFixed(3);	}
	  		else if(mod==CmdType.Shift_Y){  	now_pose[1] += parseFloat(shift);		now_pose[1] = now_pose[1].toFixed(3);	}
	  		else if(mod==CmdType.Shift_Z){  	now_pose[2] += parseFloat(shift);		now_pose[2] = now_pose[2].toFixed(3);	}
			
			//console.log('new_now_pose='+now_pose.toString() );
	  		
			$('#'+m_cmd_id).children("td.SubCmd").children("input").attr('pose',now_pose.toString());
		});
	} 
	
	
}

//----------------------------------------ROS----------------------------------------//
// Connecting to ROS

var rosip = '192.168.5.80';

var ros = new ROSLIB.Ros({
	url : 'ws://'+rosip+':9090'
});

// If there is an error on the backend, an 'error' emit will be emitted.
ros.on('error', function(error) {var request = new ROSLIB.ServiceRequest({
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


/*  Teach:SaveFile test
var request = new ROSLIB.ServiceRequest({
    cmd : "Teach:SaveFile",
    req_s : "hello\niam from web\nhello\n"
});

ui_client.callService(request, function(res) {
	console.log( 'Result : '   + res.result);
  		
});
*/

/* Teach:ReadFile test
var request = new ROSLIB.ServiceRequest({
    cmd : "Teach:ReadFile"
});

ui_client.callService(request, function(res) {
	console.log( 'res_s : '   + res.res_s);
  	
	console.log( 'Result : '   + res.result);
  		
});
*/

