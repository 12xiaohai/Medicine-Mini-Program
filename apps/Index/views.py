from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView

from apps.Index.models import Admin
from apps.UserInfo.models import UserInfo
from apps.Doctor.models import Doctor
from json import dumps


class IndexView(APIView):
    def get(self, request):
        """显示首页,使用模板"""
        return render(request, 'index.html')


class FrontLoginView(APIView):
    """前台登录"""

    def post(self, request):
        username = request.POST.get('userName')
        password = request.POST.get('password')

        try:
            # 根据用户名查询用户
            user = UserInfo.objects.get(user_name=username)

            # 明文比较输入的密码和数据库中的密码
            if password == user.password:
                # 登录成功，将用户名存入 session
                request.session['user_name'] = username  
                data = {'msg': '登录成功', 'success': True}
            else:
                data = {'msg': '登录失败：密码错误', 'success': False}
        except UserInfo.DoesNotExist:
            data = {'msg': '登录失败：用户不存在', 'success': False}

        # 返回 JSON 响应
        return HttpResponse(dumps(data, ensure_ascii=False))


class FrontLoginOutView(APIView):
    """前台登出"""

    def get(self, request):
        request.session.flush()  # 清空所有 session 数据
        return redirect(reverse("Index:index"))  # 重定向到首页


class LoginView(APIView):
    """后台登录页面"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        identify = request.POST.get('identify')

        if identify == 'admin':
            try:
                admin = Admin.objects.get(username=username)
                if password == admin.password:
                    request.session['username'] = username  # 存储用户名到 session
                    # 返回成功信息并重定向到管理员主页
                    data = {'msg': '登录成功', 'success': True, 'redirect_url': reverse('Index:main')}
                else:
                    data = {'msg': '登录失败：密码错误', 'success': False}
            except Admin.DoesNotExist:
                data = {'msg': '登录失败：用户不存在', 'success': False}
        else:  # 医生登录逻辑
            try:
                doctor = Doctor.objects.get(doctorNumber=username)
                if password == doctor.password:
                    request.session['doctorNumber'] = username  # 存储医生编号到 session
                    # 返回成功信息并重定向到医生主页
                    data = {'msg': '登录成功', 'success': True, 'redirect_url': reverse('Index:doctorMain')}
                else:
                    data = {'msg': '登录失败：密码错误', 'success': False}
            except Doctor.DoesNotExist:
                data = {'msg': '登录失败：用户不存在', 'success': False}

        return HttpResponse(dumps(data, ensure_ascii=False), content_type='application/json')



class LoginOutView(APIView):
    """后台登出"""

    def get(self, request):
        request.session.flush()  # 清空所有 session 数据
        return redirect(reverse("Index:login"))  # 重定向到登录页面


class MainView(APIView):
    """后台主界面"""

    def get(self, request):
        return render(request, 'main.html')


class DoctorMainView(APIView):
    """医生后台主界面"""

    def get(self, request):
        return render(request, 'mainDoctor.html')


class ChangePasswordView(APIView):
    """修改密码"""

    def get(self, request):
        return render(request, 'password_modify.html')

    def post(self, request):
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        new_password2 = request.POST.get('newPassword2')

        if old_password == '':
            return render(request, 'message.html', {'message': '旧密码不正确！'})
        if new_password == '':
            return render(request, 'message.html', {'message': '请输入新密码!'})
        if new_password != new_password2:
            return render(request, 'message.html', {'message': '两次新密码不一样！'})

        username = request.session.get('username')
        if not username:
            return render(request, 'message.html', {'message': '用户未登录！'})

        try:
            admin = Admin.objects.get(username=username)
            if not check_password(old_password, admin.password):
                return render(request, 'message.html', {'message': '旧密码不正确！'})

            # 更新密码
            admin.password = make_password(new_password)
            admin.save()
            return render(request, 'message.html', {'message': '密码修改成功！'})
        except Admin.DoesNotExist:
            return render(request, 'message.html', {'message': '用户不存在！'})
