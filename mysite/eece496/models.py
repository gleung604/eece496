from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    """A model to represent a student group given by a 2-character group code."""
    group_code = models.CharField(max_length=2)
    
    def __unicode__(self):
        return self.group_code

class Student(models.Model):
    """A model to represent a student. Contains name, student number,
    group and program information."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.IntegerField(unique=True)
    group = models.ForeignKey(Group)
    program = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Course(models.Model):
    """A model to represent a course."""
    course_code = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.course_code

class COGS(models.Model):
    """A model to represent a cognitive session (COGS). Contains date information."""
    name = models.CharField(max_length=5)
    date = models.DateField()
    course = models.ForeignKey(Course, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class TA(models.Model):
    """A model to represent a teaching assistant (TA). There are assumed to be 12 TAs."""
    number = models.IntegerField(unique=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

class SessionTime(models.Model):
    """A model to represent a certain session time."""
    block = models.CharField(max_length=1)
    start = models.TimeField()
    end = models.TimeField()
    
    def __unicode__(self):
        return self.block

class Session(models.Model):
    """A model to represent a specific session taking place during a COGS.
    Contains location information."""
    cogs = models.ForeignKey(COGS)
    block = models.ForeignKey(SessionTime)
    room = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.room

class Evaluation(models.Model):
    """A model to represent a specific evaluation within a session"""
    evaluatee = models.ForeignKey(Student, related_name="evaluatee_set", null=True, blank=True)
    student = models.ManyToManyField(Student, through='Attendance', related_name="evaluation_set",
                                     null=True, blank=True)
    session = models.ForeignKey(Session)
    start = models.TimeField()
    end = models.TimeField()
    ta = models.ForeignKey(TA)
    
    def __unicode__(self):
        return str(self.start)

class Attendance(models.Model):
    """A model to represent a student's attendance of an evaluation. Contains individual
    and group score information as well as absences and whether the student volunteered.
    Administrator can excuse absences."""
    student = models.ForeignKey(Student)
    evaluation = models.ForeignKey(Evaluation)
    group_score = models.IntegerField(blank=True, null=True)
    individual_score = models.IntegerField(blank=True, null=True)
    absent = models.BooleanField(default=False)
    excused = models.BooleanField(default=False)
    volunteer = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.student)
    
