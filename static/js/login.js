$(document).ready(function() {
	$(".login input").click(function(){
		$("tips").hide();
		var uname = $("#username").val();
		var pword = $("#password").val();

		if (uname.length && pword.length) {
			$.post("/manage/login",
			      {username: uname, password: pword}, 
			      function(result, status) {
				if (status != "success") {
					showTips("网络出错");
				}
				else if(result == "error_username") {
					showTips("用户名错误");
				} 
				else if (result == "error_password") {
					showTips("密码错误")
				}
				else {
					console.log("submit")
					$("form").submit();
				}
			})
		}
	})
})

// function notEmpty(uname, pword) {
// 	if (uname.length == 0) {
// 		showTips("用户名不能为空");
// 	}
// 	else if (pword.length == 0) {
// 		showTips("密码不能为空");
// 	} else {
// 		return true;
// 	}
// 	return false;
// }
function showTips(tipsTest) {
	$("#tips").text(tipsTest);
	$("#tips").fadeIn(200);
}