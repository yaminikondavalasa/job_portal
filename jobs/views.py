from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Job, Application
from .forms import ApplicationForm

def home(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(title__icontains=query) | Job.objects.filter(company__icontains=query) | Job.objects.filter(location__icontains=query)
    else:
        jobs = Job.objects.all().order_by('-posted_date')
    return render(request, 'jobs/home.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            return redirect('jobs:home')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-applied_date')
    return render(request, 'jobs/my_applications.html', {'applications': applications})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('jobs:home')
    else:
        form = UserCreationForm()
    return render(request, 'jobs/signup.html', {'form': form})