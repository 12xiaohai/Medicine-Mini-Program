# apps/Index/urls.py
from django.urls import path  # 使用 path 替代 url
from apps.Index.views import IndexView, FrontLoginView, FrontLoginOutView, LoginView, LoginOutView, MainView, DoctorMainView, ChangePasswordView

# 正在部署的应用的名称
app_name = 'Index'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # 首页
    path('frontLogin/', FrontLoginView.as_view(), name='frontLogin'),  # 前台登录
    path('frontLoginout/', FrontLoginOutView.as_view(), name='frontLoginout'),  # 前台退出
    path('login/', LoginView.as_view(), name='login'),  # 后台登录
    path('loginout/', LoginOutView.as_view(), name='loginout'),  # 后台退出
    path('main/', MainView.as_view(), name='main'),  # 后台主页面
    path('doctorMain/', DoctorMainView.as_view(), name='doctorMain'),  # 医生主页面
    path('changePassword/', ChangePasswordView.as_view(), name='changePassword')  # 管理员修改密码
]
