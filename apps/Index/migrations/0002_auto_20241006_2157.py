# Generated by Django 2.2 on 2024-10-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=128, verbose_name='登录密码'),
        ),
    ]
