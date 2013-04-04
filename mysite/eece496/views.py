# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from eece496.models import EvaluationForm, GroupForm, Attendance, AttendanceForm, Evaluation, Session, TA

@login_required
def sessions(request):
    try:
        evaluations = TA.objects.get(pk=request.user.id).evaluation_set
        sessions = Session.objects.filter(evaluation__in=evaluations.all())
    except Evaluation.DoesNotExist:
        raise Http404

    return render(request, 'eece496/session.html', {
        'session_list': sessions,
    })

@login_required
def evaluations(request, session_id):
    try:
        evaluations = Session.objects.get(pk=session_id).evaluation_set.filter(ta_id=request.user.id)
        session = Session.objects.get(pk=session_id)
    except Evaluation.DoesNotExist:
        raise Http404

    return render(request, 'eece496/evaluation.html', {
        'evaluation_list': evaluations,
        'session': session,
    })

@login_required
def attendance(request, session_id, evaluation_id):
    try:
        attendances = Attendance.objects.filter(evaluation_id=evaluation_id)
        evaluation = TA.objects.get(pk=request.user.id).evaluation_set.get(pk=evaluation_id)
        AttendanceFormSet = inlineformset_factory(Evaluation, Attendance, can_delete=False,
                                                  extra=0, form=AttendanceForm)

    except Attendance.DoesNotExist:
        return Http404
    
    if request.method == 'POST': # If the form has been submitted...
        evaluation_form = EvaluationForm(request.POST, instance=evaluation)
        print evaluation_form.errors
        group_form = GroupForm(request.POST)
        formset = AttendanceFormSet(request.POST, request.FILES, instance=evaluation) # A form bound to the POST data
        if formset.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #for form in formset:
            for form in formset:
                attendance = form.save(commit=False)
                if group_form.is_valid():
                    if attendance.absent == False:
                        group_score = group_form.cleaned_data['score']
                    else:
                        group_score = 0
                    attendance.group_score = group_score
                attendance.save()
            if evaluation_form.is_valid():
                evaluation_form.save()
                messages.success(request, 'Update successful.')
            return HttpResponseRedirect('') # Redirect after POST
    else:
        evaluation_form = EvaluationForm(instance=evaluation)
        group_form = GroupForm()
        formset = AttendanceFormSet(instance=evaluation) # An unbound form

    return render(request, 'eece496/attendance.html', {
        'evaluation_form': evaluation_form,
        'group_form': group_form,
        'formset': formset,
        'evaluation': evaluation,
    })

def selectEvaluatee(attendances):
    num_scores = None
    for attendance in attendances:
        student = attendance.student
        count = student.attendance_set.exclude(individual_score__exact=None).count()
        if num_scores == None or count < num_scores:
            num_scores = count
            evaluatee = attendances.get(student_id=student.id)
    return evaluatee
