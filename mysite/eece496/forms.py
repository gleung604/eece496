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
    score = forms.IntegerField(label='group score', required=False)

    def __init__(self, *args, **kwargs):
        evaluation = kwargs.pop('evaluation', None)
        group_score = 0
        for attendance in evaluation.attendance_set.all():
            if attendance.group_score == None:
                group_score = None
                break
            elif attendance.group_score > group_score:
                group_score = attendance.group_score
                break
        initial = kwargs.get('initial', {})
        initial['score'] = group_score
        kwargs['initial'] = initial
        super(GroupForm, self).__init__(*args, **kwargs)

class EvaluationForm(forms.ModelForm):
    "Form to input individual score for an evaluatee or volunteer"
    individual_score = forms.IntegerField(label='score', required=False)
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
            initial['volunteer'] = None
            kwargs['initial'] = initial
        elif evaluation.volunteer:
            initial = kwargs.get('initial', {})
            initial['volunteer'] = evaluation.volunteer
            initial['individual_score'] = Attendance.objects.get(student_id=evaluation.volunteer.id, evaluation_id=evaluation.id).individual_score
            initial['evaluatee'] = None
            kwargs['initial'] = initial
        elif attendance:
            initial = kwargs.get('initial', {})
            initial['evaluatee'] = attendance.student
            initial['individual_score'] = attendance.individual_score
            kwargs['initial'] = initial
        super(EvaluationForm, self).__init__(*args, **kwargs)
        # Set the queryset to the students assigned to this evaluation
        if evaluation.evaluatee:
            self.fields['evaluatee'].queryset = Student.objects.filter(pk=evaluation.evaluatee.id)
        elif attendance:
            self.fields['evaluatee'].queryset = Student.objects.filter(pk=attendance.student.id)
        attendances = Attendance.objects.filter(evaluation_id=evaluation.id)
        student_ids = []
        for attendance in attendances:
            student_ids.append(attendance.student.id)
        self.fields['volunteer'].queryset = Student.objects.filter(id__in=student_ids)

    def save(self, commit=True):
        instance = super(EvaluationForm, self).save(commit=False)
        old_attendance = None
        new_attendance = None
        # If there exists a prior entry, delete the entry
        evaluation = Evaluation.objects.get(pk=instance.id)
        # Prioritize volunteer selection over evaluatee
        if evaluation.volunteer != None or evaluation.evaluatee != None:
            if evaluation.volunteer != None:
                student = Student.objects.get(pk=evaluation.volunteer.id)
            elif evaluation.evaluatee != None:
                student = Student.objects.get(pk=evaluation.evaluatee.id)
            old_attendance = Attendance.objects.get(student_id=student.id, evaluation_id=instance.id)
            old_attendance.individual_score = None
        # Get the attendance associated with the evaluatee to save the score
        if instance.volunteer != None or instance.evaluatee != None:
            if instance.volunteer != None:
                student = Student.objects.get(pk=instance.volunteer.id)
                instance.evaluatee = None
            elif instance.evaluatee != None:
                student = Student.objects.get(pk=instance.evaluatee.id)
            new_attendance = Attendance.objects.get(student_id=student.id, evaluation_id=instance.id)
            new_attendance.individual_score = self.cleaned_data.get('individual_score')
        if commit:
            if old_attendance != None:
                old_attendance.save()
            if instance.evaluatee != None or instance.volunteer != None:
                new_attendance.save()
            instance.save()
        return instance
    
    class Meta:
        model = Evaluation
        fields = ('evaluatee', 'volunteer', 'individual_score')
