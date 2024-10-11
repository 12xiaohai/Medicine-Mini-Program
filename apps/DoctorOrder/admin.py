from django.contrib import admin
from apps.DoctorOrder.models import DoctorOrder

# Register your models here.

admin.site.register(DoctorOrder,admin.ModelAdmin)