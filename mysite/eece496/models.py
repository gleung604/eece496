from django.db import models
from django.forms import ModelForm

class TA(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.IntegerField(unique=True)
    group = models.IntegerField(default=0)
    program = models.CharField(max_length=50)
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Session(models.Model):
    ta = models.ForeignKey(TA)
    student = models.ManyToManyField(Student, through='Attendance')
    time = models.DateTimeField('session time')
    room = models.CharField(max_length=50)
    def __unicode__(self):
        return 'Location: %s' % self.room

class Attendance(models.Model):
    PRESENT_STATUS = 1
    ABSENT_STATUS = 2
    EXCUSED_STATUS = 3
    STATUS_CHOICES = (
        (PRESENT_STATUS, 'Present'),
        (ABSENT_STATUS, 'Absent'),
        (EXCUSED_STATUS, 'Excused'),
    )
    student = models.ForeignKey(Student)
    session = models.ForeignKey(Session)
    score = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PRESENT_STATUS)
    def __unicode__(self):
        return str(self.score)

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ('score', 'status')
