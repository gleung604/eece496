from django.contrib import admin
from eece496.models import TA, Student, Session, Attendance, Group, Evaluation

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 3

class SessionAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]

admin.site.register(TA)
admin.site.register(Student)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance)
admin.site.register(Group)
admin.site.register(Evaluation)
