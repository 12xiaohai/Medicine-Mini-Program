// 定义保存cookie的函数
function saveCookie() {
    // 获取用户输入的信息
    var username = $('#manager').val();  // 获取用户名
    var identify = $('#identify').val(); // 获取身份（如管理员或医生）

    // 设置 cookie 有效期（如7天）
    var expiresDays = 7;
    var date = new Date();
    date.setTime(date.getTime() + expiresDays * 24 * 3600 * 1000);

    // 保存 cookie，encodeURIComponent 是为了确保 cookie 值中不会出现非法字符
    document.cookie = "username=" + encodeURIComponent(username) + ";expires=" + date.toGMTString() + ";path=/";
    document.cookie = "identify=" + encodeURIComponent(identify) + ";expires=" + date.toGMTString() + ";path=/";

    console.log('Cookie saved: username=' + username + ', identify=' + identify);
}

$(function () {
    // 获取预生成的URL
    var loginUrl = $('#loginForm').data('login-url');   // 登录的URL
    var mainUrl = $('#loginForm').data('main-url');     // 管理员主页的URL
    var doctorMainUrl = $('#loginForm').data('doctor-url');  // 医生主页的URL

    // 登录界面
    $('#login').dialog({
        title: '登录后台',
        width: 300,
        height: 245,
        modal: true,
        iconCls: 'icon-login',
        buttons: '#btn',
    });

    // 管理员帐号验证
    $('#manager').validatebox({
        required: true,
        missingMessage: '请输入管理员帐号',
        invalidMessage: '管理员帐号不得为空',
    });

    // 管理员密码验证
    $('#password').validatebox({
        required: true,
        validType: 'length[1,30]',
        missingMessage: '请输入管理员密码',
        invalidMessage: '管理员密码长度应为1-30位',
    });

    // 加载时判断验证
    if (!$('#manager').validatebox('isValid')) {
        $('#manager').focus();
    } else if (!$('#password').validatebox('isValid')) {
        $('#password').focus();
    }

    // 单击登录按钮提交表单
    $('#btn a').click(function () {
        // 验证输入
        if (!$('#manager').validatebox('isValid')) {
            $('#manager').focus();
        } else if (!$('#password').validatebox('isValid')) {
            $('#password').focus();
        } else {
            // 获取 CSRF token
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();

            // AJAX 请求
            $.ajax({
                url: loginUrl,   // 动态获取登录URL
                type: 'post',
                data: {
                    "username": $('#manager').val(),
                    "password": $('#password').val(),
                    "identify": $('#identify').val(),
                    "csrfmiddlewaretoken": csrf
                },
                dataType: "json",  // 返回数据的类型
                beforeSend: function () {
                    $.messager.progress({
                        text: '正在登录中...',
                    });
                },
                success: function (data) {
                    // 关闭加载提示
                    $.messager.progress('close');
                    if (data.success) {
                        saveCookie(); // 调用保存cookie的函数
                        if ($('#identify').val() == "admin") {
                            location.href = mainUrl;  // 登录成功后跳转到管理员主页
                        } else {
                            location.href = doctorMainUrl;  // 登录成功后跳转到医生主页
                        }
                    } else {
                        // 登录失败时弹出提示
                        $.messager.alert('登录失败！', data.msg, 'warning', function () {
                            $('#password').select();  // 选择输入框以便重新输入密码
                        });
                    }
                },
                error: function () {
                    // 请求失败时弹出错误提示
                    $.messager.alert('错误', '请求失败，请重试！', 'error');
                }
            });
        }
    });
});
