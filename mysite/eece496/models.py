from django.db import models
from django.forms import ModelForm

class TA(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Group(models.Model):
    group_id = models.CharField(max_length=2)
    def __unicode__(self):
        return 'Group: %s' % self.group_id

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.IntegerField(unique=True)
    group = models.ForeignKey(Group)
    program = models.CharField(max_length=50)
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Session(models.Model):
    student = models.ManyToManyField(Student, through='Attendance')
    time = models.DateTimeField('session time')
    room = models.CharField(max_length=50)
    def __unicode__(self):
        return 'Location: %s' % self.room

class Evaluation(models.Model):
    start = models.TimeField('start time')
    end = models.TimeField('end time')
    session = models.ForeignKey(Session)
    ta = models.ForeignKey(TA)
    group_score = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return 'Evaluation'

class Attendance(models.Model):
    PRESENT_STATUS = 1
    ABSENT_STATUS = 2
    EXCUSED_STATUS = 3
    VOLUNTEER_STATUS = 4
    STATUS_CHOICES = (
        (PRESENT_STATUS, 'Present'),
        (ABSENT_STATUS, 'Absent'),
        (EXCUSED_STATUS, 'Excused'),
        (VOLUNTEER_STATUS, 'Volunteer'),
    )
    student = models.ForeignKey(Student)
    session = models.ForeignKey(Session)
    individual_score = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PRESENT_STATUS)
    def __unicode__(self):
        return str(self.individual_score)

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ('individual_score', 'status')
