from django.contrib import admin
from eece496.models import Student, Session, Attendance, Group, Evaluation

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 3

class EvaluationAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]

admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(Group)
admin.site.register(Evaluation, EvaluationAdmin)
