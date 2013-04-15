from django import forms
from django.db import models
from eece496.models import Attendance, Evaluation, Student

class AttendanceForm(forms.ModelForm):
    "Form to take attendance of students in a session"
    def __init__(self, *args, **kwargs):
        # Limits the drop-down list to only the current student
        super(AttendanceForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['student'].queryset = Student.objects.filter(pk=instance.student.id)

    def clean_student(self):
        # Prevents a user from changing the student for this attendance
        return self.instance.student
    
    class Meta:
        model = Attendance
        fields = ('student', 'absent')
        
class GroupForm(forms.Form):
    "Form to input a group score for a session"
    score = forms.IntegerField(label='group score')

class EvaluationForm(forms.ModelForm):
    "Form to input individual score for an evaluatee or volunteer"
    individual_score = forms.IntegerField(label='score', required=False)
    volunteer = forms.BooleanField(initial=False, required=False)
    evaluation = models.ForeignKey(Evaluation)

    def __init__(self, *args, **kwargs):
        attendance = kwargs.pop('attendance', None)
        evaluation = kwargs.get('instance', {})
        # If the evaluation already has an evaluatee/volunteer, set the initial
        # field values to reflect this information. Otherwise, we suggest an
        # evaluatee and pre-populate the fields accordingly
        if evaluation.evaluatee:
            initial = kwargs.get('initial', {})
            initial['evaluatee'] = evaluation.evaluatee
            initial['individual_score'] = Attendance.objects.get(student_id=evaluation.evaluatee.id, evaluation_id=evaluation.id).individual_score
            initial['volunteer'] = Attendance.objects.get(student_id=evaluation.evaluatee.id, evaluation_id=evaluation.id).volunteer
            kwargs['initial'] = initial
        elif attendance:
            initial = kwargs.get('initial', {})
            initial['evaluatee'] = attendance.student
            initial['individual_score'] = attendance.individual_score
            kwargs['initial'] = initial
        super(EvaluationForm, self).__init__(*args, **kwargs)
        # Set the queryset to the students assigned to this evaluation
        attendances = Attendance.objects.filter(evaluation_id=evaluation.id)
        student_ids = []
        for attendance in attendances:
            student_ids.append(attendance.student.id)
        self.fields['evaluatee'].queryset = Student.objects.filter(id__in=student_ids)
        print self.fields['evaluatee'].queryset

    def save(self, commit=True):
        instance = super(EvaluationForm, self).save(commit=False)
        # Get the attendance associated with the evaluatee to save the score
        evaluatee = Student.objects.get(pk=instance.evaluatee.id)
        attendance = Attendance.objects.get(student_id=evaluatee.id, evaluation_id=instance.id)
        attendance.individual_score = self.cleaned_data.get('individual_score')
        attendance.volunteer = self.cleaned_data.get('volunteer')
        attendance.save()
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = Evaluation
        fields = ('evaluatee', 'individual_score', 'volunteer')
