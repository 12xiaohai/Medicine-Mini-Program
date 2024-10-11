from django.contrib.auth.hashers import make_password
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from apps.Department.models import Department
from apps.Doctor.models import Doctor
from django.core.paginator import Paginator
from django.http import FileResponse
import pandas as pd
from django.conf import settings
import os

from apps.SchoolRecord.models import SchoolRecord


class FrontListView(View):
    def get(self, request):
        doctors = Doctor.objects.all()

        # 查询参数过滤
        doctorNumber = request.GET.get('doctorNumber', '')
        name = request.GET.get('name', '')
        sex = request.GET.get('sex', '')
        zhicheng = request.GET.get('zhicheng', '')
        departmentObj = request.GET.get('departmentObj', '')
        schoolRecordObj = request.GET.get('schoolRecordObj', '')

        if doctorNumber:
            doctors = doctors.filter(doctorNumber__icontains=doctorNumber)
        if name:
            doctors = doctors.filter(name__icontains=name)
        if sex:
            doctors = doctors.filter(sex=sex)
        if zhicheng:
            doctors = doctors.filter(zhicheng__icontains=zhicheng)
        if departmentObj:
            doctors = doctors.filter(departmentObj__departmentNo=departmentObj)
        if schoolRecordObj:
            doctors = doctors.filter(schoolRecordObj__schoolRecordId=schoolRecordObj)

        # 分页处理
        paginator = Paginator(doctors, 10)  # 每页显示10条记录
        page = request.GET.get('page', 1)
        doctors_page = paginator.get_page(page)

        # 查询所有科室和学历信息用于表单
        departments = Department.objects.all()
        schoolRecords = SchoolRecord.objects.all()

        context = {
            'doctors': doctors_page,
            'departments': departments,
            'schoolRecords': schoolRecords,
            'currentPage': doctors_page.number,
            'totalPage': doctors_page.paginator.num_pages,
            'recordNumber': doctors_page.paginator.count,
            'doctorNumber': doctorNumber,
            'name': name,
            'sex': sex,
            'zhicheng': zhicheng,
            'departmentObj': departmentObj,
            'schoolRecordObj': schoolRecordObj,
        }
        return render(request, 'Doctor/front_list.html', context)


class FrontAddView(View):
    def get(self, request):
        # 显示添加表单
        return render(request, 'Doctor/front_add.html')

    def post(self, request):
        # 处理添加逻辑
        doctorNumber = request.POST.get('doctorNumber')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        zhicheng = request.POST.get('zhicheng')
        telphone = request.POST.get('telphone')
        inDate = request.POST.get('inDate')
        doctorDesc = request.POST.get('doctorDesc')
        # 处理图片上传
        doctorPhoto = request.FILES.get('doctorPhoto')

        # 创建医生对象并保存
        Doctor.objects.create(
            doctorNumber=doctorNumber, name=name, sex=sex, age=age, zhicheng=zhicheng,
            telphone=telphone, inDate=inDate, doctorDesc=doctorDesc, doctorPhoto=doctorPhoto
        )
        return redirect('Doctor:frontList')


class UpdateView(View):
    def get(self, request, doctorNumber):
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        context = {
            'doctor': doctor
        }
        return render(request, 'Doctor/front_modify.html', context)

    def post(self, request, doctorNumber):
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        doctor.name = request.POST.get('name')
        doctor.sex = request.POST.get('sex')
        doctor.age = request.POST.get('age')
        doctor.zhicheng = request.POST.get('zhicheng')
        doctor.telphone = request.POST.get('telphone')
        doctor.inDate = request.POST.get('inDate')
        doctor.doctorDesc = request.POST.get('doctorDesc')

        # 更新照片
        if request.FILES.get('doctorPhoto'):
            doctor.doctorPhoto = request.FILES.get('doctorPhoto')

        doctor.save()  # 保存修改
        return redirect('Doctor:frontList')


class DeletesView(View):
    def post(self, request):
        doctorNumbers = request.POST.getlist('doctorNumbers')
        Doctor.objects.filter(doctorNumber__in=doctorNumbers).delete()
        return JsonResponse({'message': '删除成功！'})


class ListView(View):
    def get(self, request):
        doctors = Doctor.objects.all()
        paginator = Paginator(doctors, 10)  # 每页显示10条数据
        page = request.GET.get('page', 1)
        doctors_page = paginator.get_page(page)
        context = {
            'doctors_page': doctors_page
        }
        return render(request, 'Doctor/list.html', context)


class OutToExcelView(View):
    def get(self, request):
        doctors = Doctor.objects.all()
        doctorList = []
        for doctor in doctors:
            doctorList.append({
                'doctorNumber': doctor.doctorNumber,
                'name': doctor.name,
                'sex': doctor.sex,
                'age': doctor.age,
                'zhicheng': doctor.zhicheng,
                'telphone': doctor.telphone,
                'inDate': doctor.inDate,
                'doctorDesc': doctor.doctorDesc,
            })
        # 使用pandas导出excel
        df = pd.DataFrame(doctorList)
        excel_path = os.path.join(settings.MEDIA_ROOT, 'doctors.xlsx')
        df.to_excel(excel_path, index=False)

        # 返回文件作为下载
        return FileResponse(open(excel_path, 'rb'), as_attachment=True, filename='doctors.xlsx')


class BackModifyView(View):
    def get(self, request, doctorNumber):
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        context = {
            'doctor': doctor
        }
        return render(request, 'Doctor/back_modify.html', context)

    def post(self, request, doctorNumber):
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        doctor.name = request.POST.get('name')
        doctor.sex = request.POST.get('sex')
        doctor.age = request.POST.get('age')
        doctor.zhicheng = request.POST.get('zhicheng')
        doctor.telphone = request.POST.get('telphone')
        doctor.inDate = request.POST.get('inDate')
        doctor.doctorDesc = request.POST.get('doctorDesc')

        if request.FILES.get('doctorPhoto'):
            doctor.doctorPhoto = request.FILES.get('doctorPhoto')

        doctor.save()  # 保存修改
        return redirect('Doctor:list')


class BackSelfModifyView(View):
    def get(self, request):
        doctorNumber = request.session.get('doctorNumber')
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        context = {
            'doctor': doctor
        }
        return render(request, 'Doctor/back_self_modify.html', context)

    def post(self, request):
        doctorNumber = request.session.get('doctorNumber')
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        doctor.name = request.POST.get('name')
        doctor.sex = request.POST.get('sex')
        doctor.age = request.POST.get('age')
        doctor.zhicheng = request.POST.get('zhicheng')
        doctor.telphone = request.POST.get('telphone')
        doctor.inDate = request.POST.get('inDate')
        doctor.doctorDesc = request.POST.get('doctorDesc')

        if request.FILES.get('doctorPhoto'):
            doctor.doctorPhoto = request.FILES.get('doctorPhoto')

        doctor.save()
        return redirect('Doctor:list')


class FrontModifyView(View):
    def get(self, request, doctorNumber):
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        context = {
            'doctor': doctor
        }
        return render(request, 'Doctor/front_modify.html', context)

    def post(self, request, doctorNumber):
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        doctor.name = request.POST.get('name')
        doctor.sex = request.POST.get('sex')
        doctor.age = request.POST.get('age')
        doctor.zhicheng = request.POST.get('zhicheng')
        doctor.telphone = request.POST.get('telphone')
        doctor.inDate = request.POST.get('inDate')
        doctor.doctorDesc = request.POST.get('doctorDesc')

        if request.FILES.get('doctorPhoto'):
            doctor.doctorPhoto = request.FILES.get('doctorPhoto')

        doctor.save()  # 保存修改
        return redirect('Doctor:frontList')


class ListAllView(View):
    def get(self, request):
        doctors = Doctor.objects.all()
        context = {
            'doctors': doctors
        }
        return render(request, 'Doctor/list.html', context)


class FrontShowView(View):
    def get(self, request, doctorNumber):
        doctor = Doctor.objects.get(doctorNumber=doctorNumber)
        context = {
            'doctor': doctor
        }
        return render(request, 'Doctor/front_show.html', context)


class AddView(View):
    def get(self, request):
        return render(request, 'Doctor/add.html')

    def post(self, request):
        # 获取表单数据
        doctorNumber = request.POST.get('doctorNumber')
        password = request.POST.get('password')  # 获取密码
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        zhicheng = request.POST.get('zhicheng')
        telphone = request.POST.get('telphone')
        inDate = request.POST.get('inDate')
        doctorDesc = request.POST.get('doctorDesc')
        doctorPhoto = request.FILES.get('doctorPhoto')  # 处理文件上传

        # 创建医生对象并保存到数据库
        Doctor.objects.create(
            doctorNumber=doctorNumber,
            password=make_password(password),  # 保存加密后的密码
            name=name,
            sex=sex,
            age=age,
            zhicheng=zhicheng,
            telphone=telphone,
            inDate=inDate,
            doctorDesc=doctorDesc,
            doctorPhoto=doctorPhoto
        )
        return redirect('Doctor:list')  # 提交成功后跳转到医生列表

