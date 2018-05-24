from django.db import models

# Create your models here.
# ORM
# 对象模型  <--->  关系模型
# 实体类    <--->  二维表
# 属性      <--->  列
# 实体对象  <--->  一条记录


class Dept(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=10)
    excellent = models.BooleanField(default=0,verbose_name='是否优秀')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_dept'


class Emp(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    job = models.CharField(max_length=10)
    # 自参照完整性 - 员工的主管应该是已经有员工编号的员工
    # mgr = models.ForeignKey('self',null=True, blank=True,on_delete=models.PROTECT)
    mgr = models.IntegerField(null=True, blank=True, verbose_name='主管')
    sal = models.DecimalField(max_digits=7, decimal_places=2)
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT)

    class Meta:
        db_table = 'tb_emp'
