from django.contrib import admin
from eece496.models import Group, Course, COGS, Student, Session, Attendance, Group, Evaluation

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 3

class COGSAdmin(admin.ModelAdmin):
    list_display = ('name', 'time')

class EvaluationAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]
    list_display = ('ta', 'session', 'room')

    def room(self, obj):
        return (obj.session.room)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluation', 'absent', 'excused', 'volunteer')

admin.site.register(Course)
admin.site.register(COGS, COGSAdmin)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Group)
admin.site.register(Evaluation, EvaluationAdmin)
