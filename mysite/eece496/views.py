# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from eece496.models import Session, SessionForm

def session(request, session_id):
    s = get_object_or_404(Session, pk=session_id)
    if request.method == 'POST': # If the form has been submitted...
        form = SessionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/eece496/') # Redirect after POST
    else:
        form = SessionForm(instance=s) # An unbound form

    return render(request, 'eece496/session.html', {
        'session': s,
        'form': form,
    })
