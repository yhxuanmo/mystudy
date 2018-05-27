from django.contrib import admin

from school.models import StudentInfo


class StudentInfoAdmin(admin.ModelAdmin):

    list_display = ('id', 'name','passwd', 'sex')
    search_fields = ('name',)

admin.site.register(StudentInfo,StudentInfoAdmin)