# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from eece496.models import Attendance, AttendanceForm

def attendance(request, session_id, attendance_id):
    a = get_object_or_404(Attendance, session_id=session_id, pk=attendance_id)
    if request.method == 'POST': # If the form has been submitted...
        form = AttendanceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            score = form.cleaned_data['score']
            status = form.cleaned_data['status']
            b = Attendance(id=a.id, student_id=a.student_id,
                           session_id=a.session_id, score=score, status=status)
            b.save()
            return HttpResponseRedirect('/eece496/') # Redirect after POST
    else:
        form = AttendanceForm(instance=a) # An unbound form

    return render(request, 'eece496/attendance.html', {
        'attendance': a,
        'form': form,
    })
