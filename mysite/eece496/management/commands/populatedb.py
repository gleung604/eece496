from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from datetime import date as dt
from datetime import time as tm
from eece496.models import SessionTime, Course, COGS, Group, Attendance, Evaluation, Session, Student, TA
import os.path
import csv

class Command(BaseCommand):
    args = None
    help = 'Parses data from csv files and populates the database.'

    def handle(self, *args, **options):
        # Paths of csv files
        ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
        csv_ta = os.path.join(ROOT_PATH, "..\..\csv\TA Duties.csv").replace('\\','/')
        csv_room = os.path.join(ROOT_PATH, "..\..\csv\Room Sched.csv").replace('\\','/')
        csv_e253 = os.path.join(ROOT_PATH, "..\..\csv\E253.csv").replace('\\','/')
        # Populate database with COGS and TAs
        reader = csv.reader(open(csv_ta))
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
        reader = csv.reader(open(csv_room))
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
        reader = csv.reader(open(csv_e253))
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
                            
        return "Database population successful."
