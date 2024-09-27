# candidates/models.py

from django.db import models
import datetime

class Job(models.Model):
    # title = models.CharField(max_length=255)
    # description = models.TextField()
    # location = models.CharField(max_length=255)
    # posted_on = models.DateTimeField(auto_now_add=True)
    posting_title = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    assigned_recruiter = models.CharField(max_length=255, null=True, blank=True)
    target_date = models.DateField(default=datetime.date.today)
    job_status = models.CharField(max_length=50, default='In-progress', null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    account_manager = models.CharField(max_length=255, default='Venkateswarlu Sunke', null=True, blank=True)
    date_opened = models.DateField(auto_now_add=True)
    job_type = models.CharField(max_length=50, default='Full time', null=True, blank=True)
    work_experience = models.CharField(max_length=255, null=True, blank=True)
    required_skills = models.TextField(null=True, blank=True)
    address_city = models.CharField(max_length=100, null=True, blank=True)
    address_country = models.CharField(max_length=100, null=True, blank=True)
    address_province = models.CharField(max_length=100, null=True, blank=True)
    address_postal_code = models.CharField(max_length=20, null=True, blank=True)
    revenue_per_position = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    missed_revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    number_of_positions = models.IntegerField(default=1, null=True, blank=True)
    job_description = models.TextField()

    def __str__(self):
        return self.title

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    applied_for = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
