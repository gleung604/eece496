# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from eece496.models import Attendance, AttendanceForm, Evaluation

def attendance(request, session_id, evaluation_id):
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    AttendanceFormSet = inlineformset_factory(Evaluation, Attendance, extra=0)
    if request.method == 'POST': # If the form has been submitted...
        formset = AttendanceFormSet(request.POST, request.FILES, instance=evaluation) # A form bound to the POST data
        if formset.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            formset.save()
            return HttpResponseRedirect('/eece496/') # Redirect after POST
    else:
        formset = AttendanceFormSet(instance=evaluation) # An unbound form

    return render(request, 'eece496/attendance.html', {
        'formset': formset,
    })
