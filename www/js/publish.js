var isCheckPass = {
	"#actName" : false,
	"#actTime" : false,
	"#actLoc" : false,
	"#actIntru" : false,
	"#actFor" : false,
	"#actPub" : false,
	"#actJoin" : false,
	"#actDem" : true
}

$(document).ready(function() {

	//initial the time picker
	$("#time").datetimePicker({
	  min: "2012-12-12",
	  max: "2022-12-12 12:12"
	});

	//绑定字数函数

	//活动名称
	$("#actName").keyup(function() {
		checkCounter("#actName", 2);
	});
	$("#actName").blur(function() {
		checkCounterOk("#actName");
	})
	// 时间

    $("#actTime").keyup(function() {
    	checkCounter("#actTime", 100);
    });
    $("#actTime").blur(function() {
    	checkCounterOk("#actTime");
    })

    // 地点actLoc

    $("#actLoc").keyup(function() {
    	checkCounter("#actLoc", 100);
    });
    $("#actLoc").blur(function() {
    	checkCounterOk("#actLoc");
    })

    // 活动简介

    $("#actIntru").keyup(function() {
    	checkCounter("#actIntru", 50);
    });
    $("#actIntru").blur(function() {
    	checkCounterOk("#actIntru");
    })

    //活动对象

    $("#actFor").keyup(function() {
    	checkCounter("#actFor", 30);
    });
    $("#actFor").blur(function() {
    	checkCounterOk("#actFor");
    })

    //主办方

    $("#actPub").keyup(function() {
    	checkCounter("#actPub", 50);
    });
    $("#actPub").blur(function() {
    	checkCounterOk("#actPub");
    })

    //报名方式

    $("#actJoin").keyup(function() {
    	checkCounter("#actJoin", 200);
    });
    $("#actJoin").blur(function() {
    	checkCounterOk("#actJoin");
    })

    //活动详情
	$("#actDetail").keyup(function() {
		checkCounter("#actDetail", 200);
	});
	$("#actDetail").blur(function() {
		checkCounterOk("#actDetail");
	})

	//活动要求

	$("#actDem").keyup(function() {
		checkCounter("#actDem", 100);
	});
	$("#actDem").blur(function() {
		checkCounterOk("#actDem");
	})

	//发布内容
	$(document).on('click', '#public_button', function() {
        checkNeceValid();
    })
})

// 检查字数函数
// argument: selector <string>; numOfWords <interge>
// return:null <null>
function checkCounter(selector, numOfWords) {
	var text = $(selector).val();
	var len = text.length;
	$(selector+"_counter").text(len+"");

	isCheckPass[selector] = true;
	if (len > numOfWords) {
		$(selector+"_showTips i").attr("class", "weui_icon_warn");

		$(selector+"_showTips").fadeIn(150);
		$(selector+"_showTips .warningTips").fadeIn(150);
		$(selector).val($(selector).val().substring(0,numOfWords+1));
		$(selector+"_counter").text(numOfWords+1+"");

		isCheckPass[selector] = false;
	} else {
		$(selector+"_showTips").fadeOut();
	}
}

function checkNeceValid() {
	var isValid = false;
	for (var key in isCheckPass) {
		isValid = isCheckPass[key];
	}

	if (isValid == false) {
		//提示格式错误
		$(document).on('click', '#public_button', function() {
	        $.toptip('格式有点问题，回头看看哪里错了ఠ_ఠ', 'error');
	    })
	} else {
		//发布信息
		$.showLoading("发布中");
	}
}
function checkCounterOk(selector) {
	if (isCheckPass[selector] == true) {
		$(selector+"_showTips i").attr("class", "weui_icon_success");
		$(selector+"_showTips span").hide();
		$(selector+"_showTips").fadeIn(150);
	}
}