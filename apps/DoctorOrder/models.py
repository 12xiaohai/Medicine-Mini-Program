from django.db import models
from tinymce.models import HTMLField

class DoctorOrder(models.Model):
    # 自动生成的订单编号
    orderId = models.AutoField(primary_key=True, verbose_name='订单编号')  # 自增主键
    userObj = models.CharField(max_length=20, verbose_name='用户编号')  # 用户编号
    doctorObj = models.CharField(max_length=20, verbose_name='医生编号')  # 医生编号
    orderDate = models.DateField(verbose_name='预约日期')  # 预约日期
    orderTime = models.CharField(max_length=20, verbose_name='预约时间')  # 预约时间
    telephone = models.CharField(max_length=15, verbose_name='联系电话')  # 联系电话
    reason = models.CharField(max_length=100, verbose_name='预约理由')  # 预约理由
    handState = models.CharField(max_length=20, verbose_name='处理状态')  # 处理状态
    replyContent = models.CharField(max_length=255, verbose_name='回复内容', blank=True, null=True)  # 回复内容
    addTime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')  # 添加时间

    class Meta:
        db_table = 't_DoctorOrder'  # 数据库表名
        verbose_name = '医生预约信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        return {
            'orderId': self.orderId,
            'userObj': self.userObj,
            'doctorObj': self.doctorObj,
            'orderDate': self.orderDate,
            'orderTime': self.orderTime,
            'telephone': self.telephone,
            'reason': self.reason,
            'handState': self.handState,
            'replyContent': self.replyContent,
            'addTime': self.addTime,
        }
