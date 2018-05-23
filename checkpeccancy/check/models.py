from django.db import models


# Create your models here.
class CarInfo(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    car_id = models.CharField(max_length=7, verbose_name='车牌号')
    pe_reason = models.CharField(max_length=100, verbose_name='违章原因')
    pe_date = models.DateTimeField(verbose_name='违章日期')
    punish = models.CharField(max_length=100, verbose_name='处罚方式')
    accept = models.BooleanField(default=0, verbose_name='是否受理')

    class Meta:
        db_table = 'tb_car_info'
