# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from eece496.models import COGS, Group, EvaluationForm, GroupForm, Attendance, AttendanceForm, Evaluation, Session, Student, TA
import csv

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
        evaluatee = None
        if evaluation.evaluatee == None:
            evaluatee = selectEvaluatee(attendances)

    except Attendance.DoesNotExist:
        return Http404
    
    if request.method == 'POST': # If the form has been submitted...
        evaluation_form = EvaluationForm(request.POST, instance=evaluation, evaluatee=evaluatee)
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
        evaluation_form = EvaluationForm(instance=evaluation, evaluatee=evaluatee)
        group_form = GroupForm()
        formset = AttendanceFormSet(instance=evaluation) # An unbound form

    return render(request, 'eece496/attendance.html', {
        'evaluation_form': evaluation_form,
        'group_form': group_form,
        'formset': formset,
        'evaluation': evaluation,
    })

def upload(request):
    # Populate database with COGS and TAs
    reader = csv.reader(open("C:/Users/Gary/dev/mysite/TA Duties.csv"))
    g = models.Group.objects.get(name='TA')
    ta_duties = []
    for i, row in enumerate(reader):
        ta_duties.append(row)
        if i == 3:
            for j, line in enumerate(ta_duties[0]):
                print line[0:4]
                if line[0:4] == "E253":
                    cogs, created = COGS.objects.get_or_create(name=ta_duties[0][j][4:], date=ta_duties[1][j], course=None)
                    cogs.save()
        if row[0] != '':
            username = str(row[1]).lower() + str(row[2]).lower()
            ta, created = TA.objects.get_or_create(username=username, password='password',
                                                   first_name=row[1], last_name=row[2])
            ta.save()
            g.user_set.add(ta)
    # Populate database with Session, Student, Group data
    reader = csv.reader(open("C:/Users/Gary/dev/mysite/E253.csv"))
    start = False
    time = ''
    room = ''
    group = None
    cogs = COGS.objects.get(name='COGS1')
    e253 = []
    for row in reader:
        e253.append(row)
        if "Time" in row:
            start = True
            continue
        if start:
            if row[0] != '':
                time = row[0]
            if row[1] != '':
                room = row[1]
                session, created = Session.objects.get_or_create(cogs=cogs, time=time, room=room)
                session.save()
            if row[2] != '':
                group, created = Group.objects.get_or_create(group_code=row[2])
                group.save()
            if row[3] != '':
                student, created = Student.objects.get_or_create(student_number=row[3], first_name=row[4],
                                                                 last_name=row[5], group=group)
                student.save()
    # Link TA objects to sessions/evaluations
    groups = {}
    reader = csv.reader(open("C:/Users/Gary/dev/mysite/Room Sched.csv"))
    start = False
    time = None
    session = None
    ta = None
    room_sched = []
    for row in reader:
        room_sched.append(row)
        if "EECE 261 Times " in row:
            break
        if "A/C Intra-Session Time" in row:
            start = True
            continue
                
    return render(request, 'eece496/upload.html', {
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
