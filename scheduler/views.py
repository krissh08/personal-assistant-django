# scheduler/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm, CustomUserCreationForm

def home(request):
    # This view just renders the homepage template
    return render(request, 'scheduler/home.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('dashboard')
    else:
        form = EventForm()

    user_events = Event.objects.filter(user=request.user).order_by('event_time')
    context = {
        'events': user_events,
        'form': form,
    }
    return render(request, 'scheduler/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # Use the custom form
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm() # Use the custom form
    
    context = {'form': form}
    return render(request, 'scheduler/register.html', context)