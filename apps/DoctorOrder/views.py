# apps/DoctorOrder/views.py
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse

class FrontAddView(View):
    def get(self, request):
        # 处理 GET 请求，渲染添加表单
        return render(request, 'front_add.html')  # 替换为您的实际模板

    def post(self, request):
        # 处理 POST 请求，添加数据的逻辑
        return redirect('DoctorOrder:frontList')  # 假设重定向到前台列表页面

class FrontListView(View):
    def get(self, request):
        # 处理 GET 请求，查询并渲染列表
        return render(request, 'front_list.html')  # 替换为您的实际模板

class UpdatesView(View):
    def get(self, request, doctor_number):
        # 处理 GET 请求，查询并渲染更新表单
        return render(request, 'update.html', {'doctor_number': doctor_number})

    def post(self, request, doctor_number):
        # 处理 POST 请求，更新数据的逻辑
        return redirect('DoctorOrder:frontList')  # 假设重定向到前台列表页面

class DeletesView(View):
    def post(self, request):
        # 处理删除逻辑
        # 假设您会在这里实现删除操作
        return HttpResponse("Delete operation performed.")

class FrontShowView(View):
    def get(self, request, doctor_number):
        # 显示详细信息
        return render(request, 'front_show.html', {'doctor_number': doctor_number})

class AddView(View):
    def get(self, request):
        # 显示添加信息的表单
        return render(request, 'add.html')

    def post(self, request):
        # 处理添加逻辑
        return redirect('DoctorOrder:frontList')

class ListView(View):
    def get(self, request):
        # 显示所有信息的列表
        return render(request, 'list.html')

class OutToExcelView(View):
    def get(self, request):
        # 导出信息到 Excel
        return HttpResponse("Export to Excel")

class BackModifyView(View):
    def get(self, request, doctor_number):
        # 处理后台更新的逻辑
        return render(request, 'back_modify.html', {'doctor_number': doctor_number})

class BackSelfModifyView(View):
    def get(self, request):
        # 处理后台自我更新的逻辑
        return render(request, 'back_self_modify.html')

class FrontModifyView(View):
    def get(self, request, doctor_number):
        # 处理前台修改的逻辑
        return render(request, 'front_modify.html', {'doctor_number': doctor_number})

class ListAllView(View):
    def get(self, request):
        # 显示所有数据的逻辑
        return render(request, 'list_all.html')

class UpdateView(View):
    def get(self, request, doctor_number):
        # 处理 GET 请求
        return render(request, 'update_template.html', {'doctor_number': doctor_number})

    def post(self, request, doctor_number):
        # 处理 POST 请求逻辑
        return render(request, 'update_template.html', {'doctor_number': doctor_number})