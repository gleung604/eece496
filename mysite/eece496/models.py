from django.db import models
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils import formats
from django.contrib.auth.models import User

class Group(models.Model):
    group_code = models.CharField(max_length=2)
    def __unicode__(self):
        return self.group_code

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
    student = models.ForeignKey(Student)
    evaluation = models.ForeignKey(Evaluation)
    group_score = models.IntegerField(blank=True, null=True)
    individual_score = models.IntegerField(blank=True, null=True)
    absent = models.BooleanField(default=False)
    excused = models.BooleanField(default=False)
    volunteer = models.BooleanField(default=False)
    def __unicode__(self):
        return str(self.individual_score)

class AttendanceForm(forms.ModelForm):
#    absent = forms.BooleanField()

#    def __init__(self, *args, **kwargs):
#        super(AttendanceForm, self).__init__(*args, **kwargs)
#        if self.instance.absent == True:
#            self.fields['absent'] = forms.BooleanField(initial=True, required=False)
#        else:
#            self.fields['absent'] = forms.BooleanField(initial=False, required=False)

#    def save(self, force_insert=False, force_update=False, commit=True):
#        m = super(AttendanceForm, self).save(commit=False)
#        if self.cleaned_data['absent'] == True:
#            self.instance.absent=True
#        else:
#            self.instance.absent=False
#        if commit:
#            m.save()
#        return m
    
    class Meta:
        model = Attendance
        fields = ('student', 'absent')

class GroupForm(forms.Form):
    score = forms.IntegerField(label='group score')

class EvaluateeForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('student', 'individual_score')
        

#class AttendanceForm(forms.Form):
#    PRESENT_STATUS = 1
#    ABSENT_STATUS = 2
#    absent = forms.BooleanField()
#    def save(self, students, *args, **kwargs):
#        for student in students:
#            if absent == True:
#                student.status = ABSENT_STATUS
#            else:
#                student.status = PRESENT_STATUS
#        super(AttendanceForm, self).save(*args, **kwargs)

#class BaseAttendanceFormSet(BaseInlineFormSet):
#    def add_fields(self, form, index):
#        super(BaseAttendanceFormSet, self).add_fields(form, index)
#        form.fields["group_score"] = forms.IntegerField()

#    def clean(self):
#        """Checks that all present students have the same group score"""
#        if any(self.errors):
#            return
#        score = -1
#        for i in range(0, self.total_form_count()):
#            form = self.forms[i]
#            status = form.cleaned_data['status']
#            group_score = form.cleaned_data['group_score']
#            if '2' not in status and score == -1:
#                score = group_score
#            elif '2' not in status and group_score != score:
#                raise forms.ValidationError("Students have different group scores.")
#            elif '2' in status and group_score != 0:
#                raise forms.ValidationError("Absent student has a non-zero score.")
                
