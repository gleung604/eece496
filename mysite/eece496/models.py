from django.db import models
from django import forms
from django.utils import formats
from django.contrib.auth.models import User

class Group(models.Model):
    group_id = models.CharField(max_length=2)
    def __unicode__(self):
        return self.group_id

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.IntegerField(unique=True)
    group = models.ForeignKey(Group)
    program = models.CharField(max_length=50)
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Session(models.Model):
    time = models.DateTimeField('session time')
    room = models.CharField(max_length=50)
    def __unicode__(self):
        return 'Location: %s' % self.room

class TA(User):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Evaluation(models.Model):
    student = models.ManyToManyField(Student, through='Attendance')
    session = models.ForeignKey(Session)
    start = models.DateTimeField('start time')
    end = models.DateTimeField('end time')
    duration = models.IntegerField('minutes')
    ta = models.ForeignKey(TA)
    def __unicode__(self):
        return formats.date_format(self.start, "SHORT_DATETIME_FORMAT")

class Attendance(models.Model):
    PRESENT_STATUS = 1
    ABSENT_STATUS = 2
    VOLUNTEER_STATUS = 3
    EXCUSED_STATUS = 4
    STATUS_CHOICES = (
        (PRESENT_STATUS, 'Present'),
        (ABSENT_STATUS, 'Absent'),
        (VOLUNTEER_STATUS, 'Volunteer'),
        (EXCUSED_STATUS, 'Excused'),
    )
    student = models.ForeignKey(Student)
    evaluation = models.ForeignKey(Evaluation)
    group_score = models.IntegerField(blank=True, null=True)
    individual_score = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PRESENT_STATUS)
    def __unicode__(self):
        return str(self.individual_score)

class AttendanceForm(forms.ModelForm):
    PRESENT_STATUS = 1
    ABSENT_STATUS = 2
    VOLUNTEER_STATUS = 3
    STATUS_CHOICES = (
        (PRESENT_STATUS, 'Present'),
        (ABSENT_STATUS, 'Absent'),
        (VOLUNTEER_STATUS, 'Volunteer'),
    )

    status = forms.ChoiceField(widget=forms.RadioSelect, choices=STATUS_CHOICES)

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(AttendanceForm, self).save(commit=False)
        if commit:
            m.save()
        return m
    
    class Meta:
        model = Attendance
        fields = ('student', 'status', 'individual_score')
