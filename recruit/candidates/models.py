# candidates/models.py

from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    skills = models.TextField()
    file = models.FileField(upload_to='resumes/')
    secondary_email = models.CharField(max_length=255, null=True, blank=True, default=None)
    experience_in_years=models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    current_employer=models.TextField(null=True, blank=True)
    current_job_title=models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name
