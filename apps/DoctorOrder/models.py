from django.db import models

from tinymce.models import HTMLField


class DoctorOrder(models.Model):
    doctorOrderNumber = models.CharField(max_length=20, default='', primary_key=True, verbose_name='医生编号')


    class Meta:
        db_table = 't_DoctorOrder'
        verbose_name = '医生信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        doctor = {
            'doctorNumber': self.doctorNumber,
            'password': self.password,
            'departmentObj': self.departmentObj.departmentName,
            'departmentObjPri': self.departmentObj.departmentNo,
            'name': self.name,
            'sex': self.sex,
            'age': self.age,
            'doctorPhoto': self.doctorPhoto.url,
            'schoolRecordObj': self.schoolRecordObj.schoolRecordName,
            'schoolRecordObjPri': self.schoolRecordObj.schoolRecordId,
            'zhicheng': self.zhicheng,
            'inDate': self.inDate,
            'telphone': self.telphone,
            'doctorDesc': self.doctorDesc,
        }
        return DoctorOrder

