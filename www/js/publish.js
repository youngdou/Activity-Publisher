var isCheckPass = {
	"#actName" 	: 	false,
	"#actTime" 	: 	false,
	"#actLoc" 	: 	false,
	"#actIntru" : 	false,
	"#actFor" 	: 	false,
	"#actPub" 	: 	false,
	"#actJoin" 	: 	false,
	"#actDDL" 	: 	false,
	"#actDetail": 	false,
	"#actReward" : 	true,
	"#actDem" 	: 	true
}

$(document).ready(function() {

	//initial the time picker
	$("#actDDL").datetimePicker({
	  min: "2012-12-12",
	  max: "2022-12-12 12:12",
	});

	//绑定检验函数
	bindCheck();

})
// 检查字数函数
// argument: selector <string>; numOfWords <interge>
// return:null <null>
function checkCounter(selector, numOfWords) {
	var text = $(selector).val();
	var len = text.length;
	$(selector+"_counter").text(len+"");

	if (len > numOfWords) {
		showFaild(selector);

		$(selector).val($(selector).val().substring(0,numOfWords+1));
		$(selector+"_counter").text(numOfWords+1+"");

		isCheckPass[selector] = false;
	} 
	else if (len > 0) {
		isCheckPass[selector] = true;
		$(selector+"_showTips").fadeOut();
	} else {
		isCheckPass[selector] = false;
	}
}

function checkNeceValid() {
	var validNum = 0;
	var isCheckPassLength = 0;
	for (var key in isCheckPass) {
		if (isCheckPass[key]) {
			validNum++;
		}
		isCheckPassLength++;
		// console.log(key+" "+ "\tNum: "+validNum + "\tisPassLength: "+isCheckPassLength);
	}

	if (validNum != isCheckPassLength) {
		//提示格式错误
        $.toptip('格式好像有错/漏ఠ_ఠ', 'error');
	} else {
		//发布信息
		$.showLoading("发布中");
	}
}
function checkCounterOk(selector) {
	if (isCheckPass[selector] == true ) {
		showSuccess(selector);
	} else {
		$(selector+"_showTips").hide();
	}
}

function checkMutiItem(numOfWords) {
	var len_pe = $("#PEChapter").val().length;
	var len_wel = $("#welTime").val().length;
	var len_other = $("#other").val().length;

	if ((len_other + len_wel + len_pe) == 0) {
		$("#actReward_showTips").fadeOut(150);
	} 
	else if (len_pe > numOfWords || len_wel > numOfWords || len_other > numOfWords) {
		isCheckPass["#actReward"] = false;
		//show tips
		showFaild("#actReward");
	} else {
		showSuccess("#actReward")
	}
}
function bindCheck() {
	//用json对象进行每个输入框的设置（字数长度设置）
	var options = {
		"#actName" 		: 	30,
		"#actTime" 		: 	100,
		"#actLoc"		: 	100,
		"#actIntru" 	: 	50,
		"#actFor" 		: 	30,
		"#actPub" 		: 	50,
		"#actJoin" 		: 	200,
		"#actDetail" 	: 	2,
		"#actDem" 		: 	100
	}

	//绑定 字数函数
	for (var key in options) {
		bindCheckOne(key, options[key]);
	}
	//绑定 活动奖励
	CheckActReward();
	//绑定 截止时间
	$("#actDDL").click(function() {
		checkCounter("#actDDL", 16);
		checkCounterOk("#actDDL");
		console.log("#actDDL" + 16);
	});
	//绑定 发布内容
	$(document).on('click', '#public_button', function() {
        checkNeceValid();
    });
}

function bindCheckOne(selector, numOfWords) {
	$(selector).keyup(function() {
		checkCounter(selector, numOfWords);
	});
	$(selector).blur(function() {
		checkCounterOk(selector);
	})
}
function CheckActReward() {
	//体育章
	checkOneReward("#PEChapter", 2);

	//公益时
	checkOneReward("#welTime", 2);

	//其他奖励
	checkOneReward("#other", 2);
}
function checkOneReward(selector, numOfWords) {
	$(selector).keyup(function() {
		checkCounter(selector, numOfWords);
	});
	$(selector).blur(function() {
		checkMutiItem(numOfWords);
	})
}
function showSuccess(selector) {
	$(selector+"_showTips i").attr("class", "weui_icon_success");
	$(selector+"_showTips span").hide();
	$(selector+"_showTips").fadeIn(150);
}
function showFaild(selector) {
	$(selector+"_showTips i").attr("class", "weui_icon_warn");
	$(selector+"_showTips").fadeIn(150);
	$(selector+"_showTips .warningTips").fadeIn(150);
}