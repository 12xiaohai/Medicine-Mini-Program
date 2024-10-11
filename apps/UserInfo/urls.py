from apps.UserInfo.views import FrontAddView, FrontListView, UpdateView, DeletesView, FrontShowView, AddView, \
    ListView, OutToExcelView, BackModifyView, FrontModifyView, ListAllView
from django.urls import path  # 更新为 path

# 正在部署的应用的名称
app_name = 'UserInfo'

urlpatterns = [
    path('frontAdd/', FrontAddView.as_view(), name='frontAdd'),  # 前台添加
    path('frontModify/<str:user_name>/', FrontModifyView.as_view(), name='frontModify'),  # 前台更新
    path('frontList/', FrontListView.as_view(), name='frontList'),  # 前台查询列表
    path('frontShow/<str:user_name>/', FrontShowView.as_view(), name='frontShow'),  # 前台显示详情页
    path('listAll/', ListAllView.as_view(), name='listAll'),  # 前台查询所有信息
    path('update/<str:user_name>/', UpdateView.as_view(), name='update'),  # Ajax方式更新记录
    path('add/', AddView.as_view(), name='add'),  # 后台添加
    path('backModify/<str:user_name>/', BackModifyView.as_view(), name='backModify'),  # 后台更新
    path('list/', ListView.as_view(), name='list'),  # 后台信息列表
    path('deletes/', DeletesView.as_view(), name='deletes'),  # 删除记录信息
    path('OutToExcel/', OutToExcelView.as_view(), name='OutToExcel')  # 导出信息到excel并下载
]
