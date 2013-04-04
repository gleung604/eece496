from django.contrib import admin
from eece496.models import Group, Course, COGS, Student, Session, Attendance, Group, Evaluation

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 3

class EvaluationAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]
    list_display = ('id', 'room')

    def room(self, obj):
        return (obj.session.room)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluation', 'individual_score', 'absent')

admin.site.register(Course)
admin.site.register(COGS)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(Group)
admin.site.register(Evaluation, EvaluationAdmin)
