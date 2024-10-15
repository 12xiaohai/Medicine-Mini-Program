from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.paginator import Paginator
import pandas as pd
import os
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from apps.Department.models import Department
from apps.DoctorOrder.models import DoctorOrder

class FrontListView(View):
    """查询并显示医生订单列表"""

    def get(self, request):
        # 获取所有医生订单
        orders = DoctorOrder.objects.all()

        # 查询参数过滤
        doctorOrderNumber = request.GET.get('doctorOrderNumber', '')
        userObj = request.GET.get('userObj', '')  # 用户编号
        doctorObj = request.GET.get('doctorObj', '')  # 医生编号

        if doctorOrderNumber:
            orders = orders.filter(doctorOrderNumber__icontains=doctorOrderNumber)
        if userObj:
            orders = orders.filter(userObj__icontains=userObj)
        if doctorObj:
            orders = orders.filter(doctorObj__icontains=doctorObj)

        # 分页处理
        paginator = Paginator(orders, 10)  # 每页10条记录
        page = request.GET.get('page', 1)
        orders_page = paginator.get_page(page)

        # 获取科室信息用于筛选表单
        departments = Department.objects.all()

        context = {
            'orders': orders_page,
            'departments': departments,
            'currentPage': orders_page.number,
            'totalPage': orders_page.paginator.num_pages,
            'recordNumber': orders_page.paginator.count,
        }
        return render(request, 'DoctorOrder/front_list.html', context)

class FrontAddView(View):
    """添加医生订单"""

    def get(self, request):
        departments = Department.objects.all()
        return render(request, 'DoctorOrder/front_add.html', {'departments': departments})

    def post(self, request):
        # 获取表单数据并保存
        try:
            doctorOrderNumber = request.POST.get('doctorOrderNumber')
            userObj = request.POST.get('userObj')
            doctorObj = request.POST.get('doctorObj')
            orderDate_str = request.POST.get('orderDate')  # 确保格式正确
            orderDate = datetime.strptime(orderDate_str, '%Y-%m-%d').date()  # 转换为日期对象
            orderTime = request.POST.get('orderTime')
            telephone = request.POST.get('telephone')
            reason = request.POST.get('reason')
            handState = request.POST.get('handState')
            replyContent = request.POST.get('replyContent', '')  # 默认为空

            # 创建订单并保存
            DoctorOrder.objects.create(
                doctorOrderNumber=doctorOrderNumber,
                userObj=userObj,
                doctorObj=doctorObj,
                orderDate=orderDate,
                orderTime=orderTime,
                telephone=telephone,
                reason=reason,
                handState=handState,
                replyContent=replyContent
            )
            messages.success(request, "医生订单添加成功！")
            return redirect('DoctorOrder:frontList')
        except Exception as e:
            messages.error(request, f"添加失败: {str(e)}")
            return redirect('DoctorOrder:frontAdd')

class UpdateView(View):
    """更新医生订单"""

    def get(self, request, doctorOrderNumber):
        order = get_object_or_404(DoctorOrder, doctorOrderNumber=doctorOrderNumber)
        departments = Department.objects.all()
        return render(request, 'DoctorOrder/update.html', {'order': order, 'departments': departments})

    def post(self, request, doctorOrderNumber):
        try:
            order = get_object_or_404(DoctorOrder, doctorOrderNumber=doctorOrderNumber)
            order.userObj = request.POST.get('userObj')
            order.doctorObj = request.POST.get('doctorObj')
            order.orderDate = datetime.strptime(request.POST.get('orderDate'), '%Y-%m-%d').date()  # 转换为日期对象
            order.orderTime = request.POST.get('orderTime')
            order.telephone = request.POST.get('telephone')
            order.reason = request.POST.get('reason')
            order.handState = request.POST.get('handState')
            order.replyContent = request.POST.get('replyContent', '')  # 默认为空

            order.save()
            messages.success(request, "订单更新成功！")
            return redirect('DoctorOrder:frontList')
        except Exception as e:
            messages.error(request, f"更新失败: {str(e)}")
            return redirect('DoctorOrder:update', doctorOrderNumber=doctorOrderNumber)

class DeletesView(View):
    """删除医生订单"""

    def post(self, request):
        orderNumbers = request.POST.getlist('doctorOrderNumber')
        DoctorOrder.objects.filter(doctorOrderNumber__in=orderNumbers).delete()
        return JsonResponse({'message': '删除成功！'})

class ListView(View):
    """显示所有医生订单列表"""

    def get(self, request):
        orders = DoctorOrder.objects.all()
        paginator = Paginator(orders, 10)  # 每页10条记录
        page = request.GET.get('page', 1)
        orders_page = paginator.get_page(page)
        return render(request, 'DoctorOrder/list.html', {'orders_page': orders_page})

class OutToExcelView(View):
    """导出订单到 Excel 文件"""

    def get(self, request):
        orders = DoctorOrder.objects.all()
        orderList = [
            {
                'orderId': order.orderId,
                'userObj': order.userObj,
                'doctorObj': order.doctorObj,
                'orderDate': order.orderDate,
                'orderTime': order.orderTime,
                'telephone': order.telephone,
                'reason': order.reason,
                'handState': order.handState,
                'replyContent': order.replyContent,
                'addTime': order.addTime,
            }
            for order in orders
        ]
        df = pd.DataFrame(orderList)
        excel_path = os.path.join(settings.MEDIA_ROOT, 'doctor_orders.xlsx')
        df.to_excel(excel_path, index=False)
        return FileResponse(open(excel_path, 'rb'), as_attachment=True, filename='doctor_orders.xlsx')

class BackModifyView(View):
    """后台更新医生订单"""

    def get(self, request, doctorOrderNumber):
        order = get_object_or_404(DoctorOrder, doctorOrderNumber=doctorOrderNumber)
        departments = Department.objects.all()
        return render(request, 'DoctorOrder/back_modify.html', {'order': order, 'departments': departments})

    def post(self, request, doctorOrderNumber):
        order = get_object_or_404(DoctorOrder, doctorOrderNumber=doctorOrderNumber)
        order.userObj = request.POST.get('userObj')
        order.doctorObj = request.POST.get('doctorObj')
        order.orderDate = datetime.strptime(request.POST.get('orderDate'), '%Y-%m-%d').date()  # 转换为日期对象
        order.orderTime = request.POST.get('orderTime')
        order.telephone = request.POST.get('telephone')
        order.reason = request.POST.get('reason')
        order.handState = request.POST.get('handState')
        order.replyContent = request.POST.get('replyContent', '')  # 默认为空

        order.save()
        return redirect('DoctorOrder:list')

class FrontShowView(View):
    """显示订单详情"""

    def get(self, request, doctorOrderNumber):
        order = get_object_or_404(DoctorOrder, doctorOrderNumber=doctorOrderNumber)
        return render(request, 'DoctorOrder/front_show.html', {'order': order})

class BackSelfModifyView(View):
    """后台自我更新"""

    def get(self, request):
        orderNumber = request.session.get('doctorOrderNumber')
        order = get_object_or_404(DoctorOrder, doctorOrderNumber=orderNumber)
        return render(request, 'DoctorOrder/back_self_modify.html', {'order': order})

    def post(self, request):
        orderNumber = request.session.get('doctorOrderNumber')
        order = get_object_or_404(DoctorOrder, doctorOrderNumber=orderNumber)
        order.userObj = request.POST.get('userObj')
        order.reason = request.POST.get('reason')
        order.handState = request.POST.get('handState')
        order.replyContent = request.POST.get('replyContent', '')  # 默认为空

        order.save()
        return redirect('DoctorOrder:list')

class ListAllView(View):
    """显示所有订单"""

    def get(self, request):
        orders = DoctorOrder.objects.all()
        return render(request, 'DoctorOrder/list_all.html', {'orders': orders})

class AddView(View):
    """添加医生订单"""

    def get(self, request):
        # 获取所有科室信息以便选择
        departments = Department.objects.all()
        return render(request, 'DoctorOrder/add.html', {'departments': departments})

    def post(self, request):
        # 处理表单提交
        userObj = request.POST.get('userObj')
        doctorObj = request.POST.get('doctorObj')
        orderDate = request.POST.get('orderDate')  # 确保格式正确
        orderTime = request.POST.get('orderTime')
        telephone = request.POST.get('telephone')
        reason = request.POST.get('reason')
        handState = request.POST.get('handState')
        replyContent = request.POST.get('replyContent', '')  # 默认为空
        doctorPhoto = request.FILES.get('doctorPhoto')  # 可选字段

        # 创建新的医生订单
        DoctorOrder.objects.create(
            userObj=userObj,
            doctorObj=doctorObj,
            orderDate=datetime.strptime(orderDate, '%Y-%m-%d').date(),  # 转换为日期对象
            orderTime=orderTime,
            telephone=telephone,
            reason=reason,
            handState=handState,
            replyContent=replyContent,
            doctorPhoto=doctorPhoto
        )
        messages.success(request, "医生订单添加成功！")
        return redirect('DoctorOrder:frontList')

class FrontModifyView(View):
    """前台修改医生订单信息"""

    def get(self, request, orderId):
        # 获取医生订单信息
        order = get_object_or_404(DoctorOrder, orderId=orderId)
        return render(request, 'DoctorOrder/front_modify.html', {'order': order})

    def post(self, request, orderId):
        # 更新医生订单信息
        order = get_object_or_404(DoctorOrder, orderId=orderId)
        order.userObj = request.POST.get('userObj')
        order.doctorObj = request.POST.get('doctorObj')
        order.orderDate = datetime.strptime(request.POST.get('orderDate'), '%Y-%m-%d').date()  # 转换为日期对象
        order.orderTime = request.POST.get('orderTime')
        order.telephone = request.POST.get('telephone')
        order.reason = request.POST.get('reason')
        order.handState = request.POST.get('handState')
        order.replyContent = request.POST.get('replyContent', '')  # 默认为空

        if request.FILES.get('doctorPhoto'):
            order.doctorPhoto = request.FILES.get('doctorPhoto')

        order.save()  # 保存修改
        messages.success(request, "医生订单更新成功！")
        return redirect('DoctorOrder:frontList')
