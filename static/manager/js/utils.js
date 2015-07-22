function login_required () {
	var token = localStorage.getItem("token");
	if(token==null){
		window.location.href = "/qianxun/template/manager/login.html";
	} 
}


function ajax_error_catcher(XMLHttpRequest, textStatus, errorThrown){
	// 通常 textStatus 和 errorThrown 之中
	// 只有一个会包含信息	  			
	alert("An error occurred!");
}