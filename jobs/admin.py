from django.contrib import admin
from .models import Job, Application  # Application model kuda unte

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'salary', 'posted_date']
    search_fields = ['title', 'company']
    list_filter = ['location', 'posted_date']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'resume', 'applied_date']
    list_filter = ['applied_date', 'job']