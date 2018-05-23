from django.contrib import admin

# Register your models here.
from check.models import CarInfo

class CarInfoAdmin(admin.ModelAdmin):
    list_display = ('no', 'car_id', 'pe_reason', 'pe_date', 'punish', 'accept')


admin.site.register(CarInfo,CarInfoAdmin)