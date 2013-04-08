# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from django.contrib.auth.models import User
from eece496.models import SessionTime, Course, COGS, Group, EvaluationForm, GroupForm, Attendance, AttendanceForm, Evaluation, Session, Student, TA
import csv

@login_required
def sessions(request):
    try:
        evaluations = TA.objects.get(user_id=request.user.id).evaluation_set.exclude(student=None)
        sessions = Session.objects.filter(evaluation__in=evaluations.all())
    except Evaluation.DoesNotExist:
        raise Http404

    return render(request, 'eece496/session.html', {
        'session_list': sessions,
    })

@login_required
def evaluations(request, session_id):
    try:
        ta = TA.objects.get(user_id=request.user.id)
        evaluations = Session.objects.get(pk=session_id).evaluation_set.filter(ta_id=ta.id)
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
        evaluation = TA.objects.get(user_id=request.user.id).evaluation_set.get(pk=evaluation_id)
        AttendanceFormSet = inlineformset_factory(Evaluation, Attendance, can_delete=False,
                                                  extra=0, form=AttendanceForm)
        evaluatee = None
        if evaluation.evaluatee == None:
            evaluatee = selectEvaluatee(attendances)

    except Attendance.DoesNotExist:
        return Http404
    
    if request.method == 'POST': # If the form has been submitted...
        evaluation_form = EvaluationForm(request.POST, instance=evaluation, evaluatee=evaluatee)
        #print evaluation_form.errors
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
        if i == 1:
            for j, line in enumerate(ta_duties[0]):
                #print line[0:4]
                if line[0:4] == "E253":
                    cogs, created = COGS.objects.get_or_create(name=ta_duties[0][j][4:], date=ta_duties[1][j],
                                                               course=Course.objects.get(course_code=ta_duties[0][j][0:4]))
                    cogs.save()
        if row[0] != '':
            username = str(row[1]).lower() + str(row[2]).lower()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password='password')
                user.first_name = row[1]
                user.last_name = row[2]
                user.save()
            ta, created = TA.objects.get_or_create(user=user, number=row[0])
            ta.save()
            g.user_set.add(ta.user)
        if i == 16:
            times = ta_duties[i][1]
            #print times
            times = times.split(": ")
            #print times
            times = times[2].split(", ")
            #print times
            for t in times:
                session_time, created = SessionTime.objects.get_or_create(block=t[0], time=t[2:])
                session_time.save()
        
    # Link TA objects to sessions/evaluations
    groups = {}
    reader = csv.reader(open("C:/Users/Gary/dev/mysite/Room Sched.csv"))
    start = False
    time = None
    session = None
    ta = None
    room_sched = []
    for i, row in enumerate(reader):
        room_sched.append(row)
        if "EECE 261 Times " in row:
            break
    # Populate database with Session, Student, Group data
    reader = csv.reader(open("C:/Users/Gary/dev/mysite/E253.csv"))
    start = False
    time = ''
    room = ''
    evaluation = None
    attendance = None
    group = None
    cogs = None
    e253 = []
    for row in reader:
        e253.append(row)
        if "Time" in row:
            start = True
            continue
        if start:
            for cogs in COGS.objects.all():
                if row[0] != '':
                    time = row[0]
                if row[1] != '':
                    room = row[1]
                session, created = Session.objects.get_or_create(cogs=cogs, time=SessionTime.objects.get(time=time),
                                                                     room=room)
                session.save()
                table = None
                if session.time.block in room_sched[2][0][0:3]:
                    table = room_sched[2:10]
                elif session.time.block in room_sched[11][0][0:3]:
                    table = room_sched[11:19]
                if table != None:
                    for j, heading in enumerate(table[0]):
                        # Get list of TAs for a session time
                        if room[5:8] == heading[1:]:
                            for i, ta_list in enumerate(table[2:]):
                                # Check TA assignment for that session
                                for k, temp in enumerate(ta_duties[0]):
                                    if temp[4:] == cogs.name and temp[0:4] == cogs.course.course_code:
                                        for l, ta_assignment in enumerate(ta_duties[3:15]):
                                            if ta_assignment[k] == ta_list[j][2]:
                                                ta = TA.objects.get(number=ta_assignment[0])
                                                break
                                        break
                                # Create an evaluation with the selected TA for this session
                                evaluation, created = Evaluation.objects.get_or_create(session=session, time=ta_list[0],
                                                                                  ta=ta)
                                evaluation.save()
                            break
                if row[2] != '':
                    group, created = Group.objects.get_or_create(group_code=row[2])
                    group.save()
                if row[3] != '':
                    student, created = Student.objects.get_or_create(student_number=row[3], first_name=row[4],
                                                                 last_name=row[5], group=group)
                    student.save()
                    for evaluation in session.evaluation_set.all():
                        attendance, created = Attendance.objects.get_or_create(student=student, evaluation=evaluation)
                        attendance.save()
                
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
