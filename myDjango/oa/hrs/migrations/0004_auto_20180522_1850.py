# Generated by Django 2.0.5 on 2018-05-22 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrs', '0003_emp_mgr'),
    ]

    operations = [
        migrations.AddField(
            model_name='dept',
            name='excellent',
            field=models.BooleanField(default=0, verbose_name='是否优秀'),
        ),
        migrations.AlterField(
            model_name='emp',
            name='comm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='emp',
            name='mgr',
            field=models.IntegerField(blank=True, null=True, verbose_name='主管'),
        ),
    ]
