var isCheckPass = {
	"#actName" 	: 	false,
	"#actTime" 	: 	false,
	"#actLoc" 	: 	false,
	"#actIntru" : 	false,
	"#actFor" 	: 	false,
	"#actPub" 	: 	false,
	"#actJoin" 	: 	false,
	"#actDDL" 	: 	false,
	"#actDetail": 	false
}

$(document).ready(function() {

	//initial the time picker
	$("#actDDL").datetimePicker({
	  min: theDate(),
	  max: "2022-12-12 12:12",
	});

	//绑定检验函数
	bindCheck();
	UpLoadImage();
});

// 当前时间--活动截止如期不得提前于当前时间
function theDate() {
	var timeStr = "";
	var Today = new Date();
	timeStr = Today.getFullYear()+"-"+
				(Today.getMonth()+1)+"-"+
				(Today.getDate()) + " "+
				(Today.getHours()) + ":"+
				(Today.getMinutes());

	return timeStr;
}

function UpLoadImage() {
	$.weui = {};
	$.weui.alert = function(options){
	    options = $.extend({title: '警告', text: '警告内容'}, options);
	    var $alert = $('.weui_dialog_alert');
	    $alert.find('.weui_dialog_title').text(options.title);
	    $alert.find('.weui_dialog_bd').text(options.text);
	    $alert.on('touchend click', '.weui_btn_dialog', function(){
	        $alert.hide();
	    });
	    $alert.show();
	};
	// 1024KB，也就是 1MB
	var maxSize = 1024 * 1024;
	// 图片最大宽度
	var maxWidth = 600;
	// 最大上传图片数量
	var maxCount = 1;
	$('.js_file').on('change', function (event) {
	    var files = event.target.files;

	    // 如果没有选中文件，直接返回
	    if (files.length === 0) {
	        return;
	    }
	    for (var i = 0, len = files.length; i < len; i++) {
	        var file = files[i];
	        var reader = new FileReader();

	        if (file.size > maxSize) {
	            $.toptip("图片大于1M", "error");
	            continue;
	        }

	        if ($('.weui_uploader_file').length >= maxCount) {
	            $.weui.alert({text: '最多只能上传' + maxCount + '张图片'});
	            return;
	        }

	        reader.onload = function (e) {
	            var img = new Image();
	            img.onload = function () {
	                // 不要超出最大宽度
	                var w = Math.min(maxWidth, img.width);
	                // 高度按比例计算
	                var h = img.height * (w / img.width);
	                var canvas = document.createElement('canvas');
	                var ctx = canvas.getContext('2d');
	                // 设置 canvas 的宽度和高度
	                canvas.width = w;
	                canvas.height = h;
	                ctx.drawImage(img, 0, 0, w, h);
	                var base64 = canvas.toDataURL('image/png');

	                // 插入到预览区
	                var $preview = $('<li class="weui_uploader_file weui_uploader_status" style="background-image:url(' + base64 + ')"><div class="weui_uploader_status_content">0%</div></li>');
	                $('.weui_uploader_files').append($preview);
	                var num = $('.weui_uploader_file').length;
	                $('.js_counter').text(num + '/' + maxCount);

	                // 然后假装在上传，可以post base64格式，也可以构造blob对象上传，也可以用微信JSSDK上传
	                var test_result = "nerver_back";
	                var test_status = "success";
	                $.post("/uploadImage", {base64Image: base64}, function(result, status) {
	                  console.log("result: "+result+"\nstatus: "+status);
	                  //result返回值说明：
	                  //图片成功存储在后台，则返回图片的文件名xxx_x.png
	                  //图片写入有误则返回字符串 UploadError

	                  // test_result的存在是为了保存返回值到函数外部以便使用
	                  // test_result 初始为nerver_back 用于判断是否在回调中返回了值
	                  test_result = result;
	                  test_status = status;
	                })
	                var progress = 0;
	                function uploading() {
	                	//忙等待，阻塞，等待post返回值
	                	for (var i = 0; test_result == "nerver_back" && i < 20000; i++) {
	                		console.log("wait...");
	                	}

	                	$preview.find('.weui_uploader_status_content').text("压缩\n"+ (++progress) + '%');
	                	if (progress < 100 && test_result != "UploadError" && test_status == "success") {
	                	    setTimeout(uploading, 30);
	                	}
	                	else if (test_result == "UploadError" || test_status != "success") {
	                	    // 如果是失败，塞一个失败图标
	                	    $preview.find('.weui_uploader_status_content').html('<i class="weui_icon_warn"></i>');

	                	    $.toptip('图片上传失败', 'error');
	                	    setTimeout(function() {
	                	    	$("weui_uploader_file").hide(1000);
	                	    	$('.weui_uploader_files').remove();	    
	                	    }, 1200);
	                	} else {
	                		$preview.removeClass('weui_uploader_status').find('.weui_uploader_status_content').remove();
	                	}
	                	//
	                	if (test_result != "UploadError" && test_status == "success" && progress==100) {
	                		$(".weui_uploader_input_wrp").hide();

	                		// 将图片文件名嵌入表单中，方便上传
	                		var $ImageForm = $("<input  id=\"QRImageName\" name=\"QRImageName\" "+ "value ="+test_result+" type=\"text\">");
	                		$("#actDetail").append($ImageForm);

	                		$.toptip("图片上传成功", "success");
	                	}
	                }
	                setTimeout(uploading, 30);

	            }
	            img.src = e.target.result;
	        }
	        reader.readAsDataURL(file);
	    }
	});
}

// 检查字数函数
// argument: selector <string>; numOfWords <interge>
// return:null <null>
function checkCounter(selector, numOfWords) {
	// 当前文本框内的文字数量
	var text = $(selector).val();
	var len = text.length;
	$(selector+"_counter").text(len+"");

	// 字数已满，提醒用户
	if (len == numOfWords) {
		showFaild(selector);

		$(selector).val($(selector).val().substring(0,numOfWords+1));
		$(selector+"_counter").text(numOfWords+1+"");

		isCheckPass[selector] = false;
	} 
	else if (len > 0) {
		// 输入正确，隐藏警告信息
		// isCheckPass[selector] = true;
		$(selector+"_showTips").fadeOut();
	}
	else {
		//len == 0
	}
}

function checkNeceValid() {
	// 9个必填项目
	var validNum = 9;

	var isCheckPassLength = 0;
	for (var key in isCheckPass) {
		if ($(key).val().length != 0) {
			isCheckPassLength++;
		}

	}

	// 1. 先检查字数没问题
	if (validNum != isCheckPassLength) {
		//提示格式错误
		checkEmpty();
        $.toptip('输入格式有错/漏(` V`)', 'error');
	} else {
	//2. 检查活动名称是否重复
		$.post("/checkActName", {actName: $("#actName").val()}, function(result, status) {
			//当数据库中 *不存在* 这个活动名称时
			//result = no_exist
			//否则
			//result = exist
			if (status == "success" && result == "no_exist") {
				//发布信息
				$.showLoading("发布中");
				$("#Actform").submit();
			} else {
				//
				$.toptip("活动名称和别人重复啦~", 'error');
				return;
			}
		})
	}
}
function checkCounterOk(selector) {
	if ($(selector).val().length != 0) {
		showSuccess(selector);
	}
	else if (isCheckPass[selector] == true) {
		$(selector+"_showTips").hide();
	}

}
// 给相关的输入框绑定具体事件
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
		"#actDetail" 	: 	200,
	}

	//绑定 检测函数
	for (var key in options) {
		bindCheckOne(key, options[key]);
	}
	//截止时间
	$("#actDDL").click(function() {
		checkCounter("#actDDL", 17);
		checkCounterOk("#actDDL");
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

function showSuccess(selector) {
	$(selector+"_showTips i").attr("class", "weui_icon_success");
	$(selector+"_showTips span").hide();
	$(selector+"_showTips").fadeIn(150);
}
function showFaild(selector) {
	if (arguments.length == 2) {
		var warnTipsText = arguments[1];
	} else {
		var warnTipsText="字数已满";
	}
	// 显示提醒框
	$(selector+"_showTips .warningTips").text(warnTipsText);
	$(selector+"_showTips i").attr("class", "weui_icon_warn");
	$(selector+"_showTips").fadeIn(150);
	$(selector+"_showTips .warningTips").fadeIn(150);
}
function checkEmpty() {
	for (var key in isCheckPass) {
		if ($(key).val().length == 0) {
			showFaild(key, "请输入相关内容");
		}
	}
}
