# Generated by Django 2.2.28 on 2024-10-14 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorOrder',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False, verbose_name='订单编号')),
                ('userObj', models.CharField(max_length=20, verbose_name='用户编号')),
                ('doctorObj', models.CharField(max_length=20, verbose_name='医生编号')),
                ('orderDate', models.DateField(verbose_name='预约日期')),
                ('orderTime', models.CharField(max_length=20, verbose_name='预约时间')),
                ('telephone', models.CharField(max_length=15, verbose_name='联系电话')),
                ('reason', models.CharField(max_length=100, verbose_name='预约理由')),
                ('handState', models.CharField(max_length=20, verbose_name='处理状态')),
                ('replyContent', models.CharField(blank=True, max_length=255, null=True, verbose_name='回复内容')),
                ('addTime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '医生预约信息',
                'verbose_name_plural': '医生预约信息',
                'db_table': 't_DoctorOrder',
            },
        ),
    ]