function login_required () {
	var token = localStorage.getItem("token");
	if(token==null){
		window.location.href = "/qianxun/template/manager/login.html";
	}
    return token;
}


function ajax_error_catcher(XMLHttpRequest, textStatus, errorThrown){
	// 通常 textStatus 和 errorThrown 之中
	// 只有一个会包含信息	  			
	alert("An error occurred!");
}



function newWindow(title,content){
    $('#window').window({
        modal:true,
        width:500,
        height:300,
        title:title,
        content:content,
        onClose:function(){
            document.getElementById("window").innerHTML="";
        }
    });
}

function newMessager(title,content){
    $.messager.alert(title,content);
}

function newNoticeDatagrid(gridName){
    $(gridName).datagrid({
        fitColumns:true,
        singleSelect:true,
        rownumbers:true,
        pagination:true,
        pageSize: 20,
        pageList: [10,20,30,40,50],
        loadMsg:'载入数据中，请稍等...',
        columns:[[   
            {field:'title',title:'标题',width:500,algin:'center',sortable:true},   
            {field:'manager',title:'作者',width:100,algin:'center',sortable:true},   
            {field:'updateTime',title:'时间',width:200,algin:'center',sortable:true}, 
            {field:'id',title:'id',hidden:true}, 
            {field:'content',title:'content',hidden:true},  
        ]]
    });
}

function getNoticeData(gridName, url, pageNumber, pageSize){
    //异步获取数据到javascript对象，入参为查询条件和页码信息 
    $.ajax({
        type: "POST",
        url: url,
        data: {token:token,page:pageNumber,count:pageSize},
        success:function(data){
            if(data.status == 0){
                var gridData = data.data;
                if(data.data.total==0){
                    newMessager("提示","暂无公告");
                }else{
                    $(gridName).datagrid('loadData', data.data); 
                }
            }else{
                newMessager("出现错误",data.data.error_info);
            }
        },
        error:function (XMLHttpRequest, textStatus, errorThrown) {
            ajax_error_catcher(XMLHttpRequest, textStatus, errorThrown);
            this; // 调用本次AJAX请求时传递的options参数
        },
    });  
}
