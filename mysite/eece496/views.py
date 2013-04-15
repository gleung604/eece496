# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from datetime import date as dt
from datetime import time as tm
from eece496.models import SessionTime, Course, COGS, Group, Attendance, Evaluation, Session, Student, TA
from eece496.forms import EvaluationForm, GroupForm, AttendanceForm
import csv

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
        evaluations = Session.objects.get(pk=session_id).evaluation_set.filter(ta_id=ta.id)
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
        group_form = GroupForm()
        formset = AttendanceFormSet(instance=evaluation) # An unbound form

    session = Session.objects.get(pk=session_id)
    evaluations = Evaluation.objects.filter(session__cogs_id=session.cogs.id, session__block=session.block,
                                            ta__user_id=request.user.id, start__gt=evaluation.start).order_by('start')
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

@login_required
def update(request):
    """A temporary function to call the python script that parses three csv files and updates
    the database with the given data."""
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
                    # Creates a COGS with the given date
                    date = datetime.strptime(ta_duties[1][j], "%b-%d")
                    date = date.replace(year=dt.today().year)
                    cogs, created = COGS.objects.get_or_create(name=ta_duties[0][j][4:], date=date,
                                                               course=Course.objects.get(course_code=ta_duties[0][j][0:4]))
                    cogs.save()
        if row[0] != '':
            # Create TA users if they do not already exist
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
            # Create session times (eg. A, B, C, D)
            times = ta_duties[i][1]
            #print times
            times = times.split(": ")
            #print times
            times = times[2].split(", ")
            #print times
            for t in times:
                time = t.split("=")
                #print time
                start, end = time[1].split("-")
                start = datetime.strptime(start, "%I%p").time()
                end = datetime.strptime(end, "%I%p").time()
                #print start, end
                session_time, created = SessionTime.objects.get_or_create(block=time[0], start=start,
                                                                          end=end)
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
    time = None
    room = None
    evaluation = None
    attendance = None
    group = None
    cogs = None
    e253 = []
    for z, row in enumerate(reader):
        e253.append(row)
        if z > 2:
            # Repeat procedure for every COGS
            for cogs in COGS.objects.all():
                # Create sessions
                if row[0] != '':
                    time = row[0]
                    start, end = time.split("-")
                    start = datetime.strptime(start, "%I%p").time()
                    end = datetime.strptime(end, "%I%p").time()
                if row[1] != '':
                    room = row[1]
                session, created = Session.objects.get_or_create(cogs=cogs, room=room,
                                                                 block=SessionTime.objects.get(start=start, end=end))
                session.save()

                # Depending on session time, select different tables in the csv file
                table = None
                if session.block.block in room_sched[2][0][0:3]:
                    table = room_sched[2:10]
                elif session.block.block in room_sched[11][0][0:3]:
                    table = room_sched[11:19]
                if table != None:
                    # Combine information from Room Sched and TA Duties files to determine TA for this session
                    for j, heading in enumerate(table[0]):
                        # Get list of TAs for a session time
                        if room[5:8] == heading[1:]:
                            for i, ta_list in enumerate(table[2:]):
                                # Check TA assignment for that session
                                for k, temp in enumerate(ta_duties[0]):
                                    # If matches current cogs
                                    if temp[4:] == cogs.name and temp[0:4] == cogs.course.course_code:
                                        for m, session_block in enumerate(ta_duties[2][k:k+4]):
                                            if session_block == session.block.block:
                                                for l, ta_assignment in enumerate(ta_duties[3:15]):
                                                    if ta_assignment[k+m] == ta_list[j][2]:
                                                        ta = TA.objects.get(number=ta_assignment[0])
                                                        break
                                                break
                                        break
                                # Create an evaluation with the selected TA for this session
                                #print ta_list[0]
                                eval_start, eval_end = ta_list[0].split("-")
                                start_hours, start_mins = eval_start.split(":")
                                end_hours, end_mins = eval_end.split(":")
                                eval_start = (datetime.combine(dt.today(), tm(session.block.start.hour, session.block.start.minute))
                                         + timedelta(hours=int(start_hours), minutes=int(start_mins))).time()
                                eval_end = (datetime.combine(dt.today(), tm(session.block.start.hour, session.block.start.minute))
                                         + timedelta(hours=int(end_hours), minutes=int(end_mins))).time()
                                evaluation, created = Evaluation.objects.get_or_create(session=session, ta=ta,
                                                                                       start=eval_start, end=eval_end)
                                evaluation.save()
                            break
                if row[2] != '':
                    # Create group
                    group, created = Group.objects.get_or_create(group_code=row[2])
                    group.save()
                if row[3] != '':
                    # Create student, add student to group, create attendace to current evaluation
                    student, created = Student.objects.get_or_create(student_number=row[3], first_name=row[5],
                                                                 last_name=row[4], group=group)
                    student.save()
                    for evaluation in session.evaluation_set.all():
                        attendance, created = Attendance.objects.get_or_create(student=student, evaluation=evaluation)
                        attendance.save()
                
    return render(request, 'eece496/update.html', {
    })
