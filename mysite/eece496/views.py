# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from eece496.models import Attendance, AttendanceForm, Evaluation, Session, TA

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
        attendances = Attendance.objects.filter(evaluation_id=evaluation_id).values()
        evaluation = TA.objects.get(pk=request.user.id).evaluation_set.get(pk=evaluation_id)
        AttendanceFormSet = inlineformset_factory(Evaluation, Attendance, can_delete=False,
                                                  extra=0, form=AttendanceForm)
    except Attendance.DoesNotExist:
        raise Http404
    
    if request.method == 'POST': # If the form has been submitted...
        formset = AttendanceFormSet(request.POST, request.FILES, instance=evaluation) # A form bound to the POST data
        if formset.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #for form in formset:
            formset.save()
            return HttpResponseRedirect('') # Redirect after POST
    else:
        formset = AttendanceFormSet(instance=evaluation) # An unbound form

    return render(request, 'eece496/attendance.html', {
        'formset': formset,
    })
