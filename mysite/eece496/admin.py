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
    date_hierarchy = 'date'

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
    list_filter = ('ta', 'session__block', 'session__room', 'session__cogs')
    list_display = ('ta', 'block', 'room', 'cogs')

    def block(self, obj):
        return obj.session.block
    block.admin_order_field = 'session__block'

    def room(self, obj):
        return obj.session.room
    room.admin_order_field = 'session__room'

    def cogs(self, obj):
        return obj.session.cogs

class StudentAdmin(admin.ModelAdmin):
    fields = (('first_name', 'last_name'), 'student_number', 'group', 'program')
    inlines = [AttendanceInline]
    search_fields = ['first_name', 'last_name', 'student_number', 'group']
    list_display = ('first_name', 'last_name', 'student_number', 'group')
    list_display_links = ('first_name', 'last_name')

class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ['student__first_name', 'student__last_name']
    list_filter = ('evaluation__start', 'absent', 'excused')
    list_display = ('student', 'session', 'absent', 'excused')

    def session(self, obj):
        return obj.evaluation.session.room

class TAAdmin(admin.ModelAdmin):
    inlines = [EvaluationInline]
    search_fields = ['user__first_name', 'user__last_name']
    list_display = ('number', 'name')
    list_display_links = ('name',)

    def name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    name.admin_order_field = 'user__first_name'

class SessionTimeAdmin(admin.ModelAdmin):
    list_display = ('block', 'start', 'end')

admin.site.register(Course, CourseAdmin)
admin.site.register(COGS, COGSAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(TA, TAAdmin)
admin.site.register(SessionTime, SessionTimeAdmin)
