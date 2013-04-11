from django.contrib import admin
from eece496.models import SessionTime, TA, Group, Course, COGS, Student, Session, Attendance, Group, Evaluation

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

class SessionInline(admin.TabularInline):
    model = Session
    extra = 0

class COGSInline(admin.TabularInline):
    model = COGS
    extra = 0

class EvaluationInline(admin.TabularInline):
    model = Evaluation
    extra = 0

class COGSAdmin(admin.ModelAdmin):
    inlines = [SessionInline]
    list_display = ('name', 'date', 'course')

class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    list_display = ('group_code',)

class SessionAdmin(admin.ModelAdmin):
    inlines = [EvaluationInline]
    list_display = ('room', 'block', 'cogs')

class CourseAdmin(admin.ModelAdmin):
    inlines = [COGSInline]
    list_display = ('course_code',)

class EvaluationAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]
    list_display = ('ta', 'block', 'room')

    def block(self, obj):
        return obj.session.block

    def room(self, obj):
        return obj.session.room

class StudentAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]
    list_display = ('first_name', 'last_name', 'student_number', 'group')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluation', 'absent', 'excused')

class TAAdmin(admin.ModelAdmin):
    inlines = [EvaluationInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(COGS, COGSAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(TA, TAAdmin)
admin.site.register(SessionTime)
