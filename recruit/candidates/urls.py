# candidates/urls.py

from django.urls import path
from .views import ResumeUploadView,getAllResumes

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('resumes/', getAllResumes, name='resume-list'), 
]
