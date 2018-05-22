from django.contrib import admin

# Register your models here.
from hrs.models import Dept, Emp


class DeptAdmin(admin.ModelAdmin):
    # 在后台显示表格
    list_display = ('no', 'name', 'location', 'excellent')
    # 指定排序方式
    ordering = ('no',)


class EmpAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'job', 'mgr', 'sal', 'comm', 'dept')
    ordering = ('no',)
    # 在后台添加搜索框
    search_fields = ('name', 'job')


# 注册后台显示的表格
admin.site.register(Dept,DeptAdmin)
admin.site.register(Emp,EmpAdmin)
