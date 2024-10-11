from django.contrib.auth.hashers import make_password
from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=20, primary_key=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='登录密码')

    class Meta:
        db_table = 't_admin'
        verbose_name = '管理员'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        # 仅在密码未加密时执行加密
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(Admin, self).save(*args, **kwargs)
