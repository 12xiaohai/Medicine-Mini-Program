"""PythonProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path  # 更新为 re_path
from django.views.static import serve  # 需要导入
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version='v1',
        description="API documentation for Your Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 这部分很重要
    re_path(r'^UserInfo/', include('apps.UserInfo.urls', namespace='UserInfo')),  # 用户信息模块
    re_path(r'^Department/', include('apps.Department.urls', namespace='Department')),  # 科室信息模块
    re_path(r'^Doctor/', include('apps.Doctor.urls', namespace='Doctor')),  # 医生信息模块  
    re_path(r'^SchoolRecord/', include('apps.SchoolRecord.urls', namespace='SchoolRecord')),  # 学历信息模块
    re_path(r'^DoctorOrder/', include('apps.DoctorOrder.urls', namespace='DoctorOrder')),  # 医生预约模块
    re_path(r'^Leaveword/', include('apps.Leaveword.urls', namespace='Leaveword')),  # 留言模块
    re_path(r'^Notice/', include('apps.Notice.urls', namespace='Notice')),  # 新闻公告模块
    re_path(r'^Patient/', include('apps.Patient.urls', namespace='Patient')),  # 病人模块
    re_path(r'^', include("apps.Index.urls", namespace="Index")),  # 首页模块
    re_path(r'^tinymce/', include('tinymce.urls')),  # TinyMCE 编辑器

    # Swagger 文档路由
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
