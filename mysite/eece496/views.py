# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from django.contrib.auth.models import User
from eece496.models import SessionTime, Course, COGS, Group, Attendance, Evaluation, Session, Student, TA
from eece496.forms import EvaluationForm, GroupForm, AttendanceForm

@login_required
def past(request):
    "Get a list of past COGS"
    cogs = COGS.objects.filter(date__lte=dt(2013, 2, 11))

    return render(request, 'eece496/cogs.html', {
        'cogs_list': cogs,
    })

@login_required
def today(request):
    "Get a list of upcoming evaluations for today"
    cogs = COGS.objects.filter(date=dt(2013, 1, 11))
    evaluations = TA.objects.get(user_id=request.user.id).evaluation_set.exclude(student=None)
    sessions = Session.objects.filter(evaluation__in=evaluations.all(), cogs__in=cogs, block__end__gte=tm(8))
    evaluations = Evaluation.objects.filter(session__in=sessions, ta__user_id=request.user.id).order_by('start')
    
    return render(request, 'eece496/today.html', {
        'cogs_list': cogs,
        'session_list': sessions,
        'evaluation_list': evaluations
    })

@login_required
def sessions(request, cogs_id):
    "Get sessions for a given COGS"
    try:
        evaluations = TA.objects.get(user_id=request.user.id).evaluation_set.exclude(student=None)
        sessions = Session.objects.filter(evaluation__in=evaluations.all(), cogs_id=cogs_id)
    except Evaluation.DoesNotExist:
        raise Http404

    return render(request, 'eece496/session.html', {
        'session_list': sessions,
        'cogs_id': cogs_id,
    })

@login_required
def evaluations(request, cogs_id, session_id):
    "Get evaluations for a given session"
    try:
        ta = TA.objects.get(user_id=request.user.id)
        evaluations = Session.objects.get(pk=session_id).evaluation_set.filter(ta_id=ta.id).exclude(student=None)
        session = Session.objects.get(pk=session_id)
    except Evaluation.DoesNotExist:
        raise Http404

    return render(request, 'eece496/evaluation.html', {
        'evaluation_list': evaluations,
        'session': session,
        'cogs_id': cogs_id,
    })

@login_required
def attendance(request, cogs_id, session_id, evaluation_id):
    "Create forms to input marks and take attendance"
    try:
        attendances = Attendance.objects.filter(evaluation_id=evaluation_id)
        evaluation = TA.objects.get(user_id=request.user.id).evaluation_set.get(pk=evaluation_id)
        AttendanceFormSet = inlineformset_factory(Evaluation, Attendance, can_delete=False,
                                                  extra=0, form=AttendanceForm)
        attendance = None
        if evaluation.evaluatee == None:
            attendance = select_evaluatee(attendances)

    except Attendance.DoesNotExist:
        return Http404
    
    if request.method == 'POST': # If the form has been submitted...
        evaluation_form = EvaluationForm(request.POST, instance=evaluation, attendance=attendance)
        group_form = GroupForm(request.POST, evaluation=evaluation)
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
                evaluation = evaluation_form.save(commit=False)
                if evaluation.volunteer != None:
                    if attendances.get(student_id=evaluation.volunteer.id).absent == True:
                        messages.error(request, 'Student is absent. Please choose another volunteer.')
                    else:
                        evaluation_form.save()
                        messages.success(request, 'Update successful.')
                elif evaluation.evaluatee != None:
                    if attendances.get(student_id=evaluation.evaluatee.id).absent == True:
                        messages.error(request, 'Student is absent. Please choose a volunteer.')
                    else:
                        evaluation_form.save()
                        messages.success(request, 'Update successful.')
                else:
                    evaluation_form.save()
                    messages.success(request, 'Update successful.')
            return HttpResponseRedirect('') # Redirect after POST
    else:
        evaluation_form = EvaluationForm(instance=evaluation, attendance=attendance)
        group_form = GroupForm(evaluation=evaluation)
        formset = AttendanceFormSet(instance=evaluation) # An unbound form

    session = Session.objects.get(pk=session_id)
    evaluations = Evaluation.objects.filter(session__cogs_id=session.cogs.id, session__block=session.block,
                                            ta__user_id=request.user.id, start__gt=evaluation.start).exclude(student=None).order_by('start')
    if evaluations.exists():
        next_evaluation = evaluations[0]
    else:
        next_evaluation = None

    return render(request, 'eece496/attendance.html', {
        'evaluation_form': evaluation_form,
        'group_form': group_form,
        'formset': formset,
        'evaluation': evaluation,
        'next_evaluation': next_evaluation,
    })

def select_evaluatee(attendances):
    """Selects an evaluatee based on the number of individual scores they have accrued and
    whether they have any excused absences. A higher count means a lower priority."""
    # Determines lowest number of scores that a student in this evaluation has
    num_scores = None
    evaluatee = None
    for attendance in attendances:
        student = attendance.student
        count = student.attendance_set.exclude(individual_score__exact=None).count()
        if num_scores == None or count < num_scores:
            num_scores = count
    # Create a queryset containing only students with the lowest number of scores
    attendance_ids = []
    excused_ids = []
    for attendance in attendances:
        student = attendance.student
        count = student.attendance_set.exclude(individual_score__exact=None).count()
        if count == num_scores:
            attendance_ids.append(attendance.id)
    # Among the chosen students, select the student with the highest number of approved absences
    num_scores = None
    prioritized_attendances = Attendance.objects.filter(id__in=attendance_ids)
    for attendance in prioritized_attendances:
        student = attendance.student
        count = student.attendance_set.exclude(excused=True).count()
        if num_scores == None or count < num_scores:
            num_scores = count
            evaluatee = attendance
    return evaluatee
