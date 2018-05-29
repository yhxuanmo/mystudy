from django.db import models

class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='姓名')
    passwd = models.CharField(max_length=20, verbose_name='密码')
    sex = models.BooleanField(default=1, verbose_name='性别')

    class Meta:
        db_table = 'tb_student_info'

