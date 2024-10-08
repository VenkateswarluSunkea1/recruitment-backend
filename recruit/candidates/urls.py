from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    CandidateListCreateView,
    CandidateDetailView,
    ResumeUploadView,
    getAllResumes,
    associate_resumes_with_job
)

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('resumes/', getAllResumes, name='resume-list'), 
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),  # List and create jobs
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),  # Retrieve, update, or delete a specific job

    # Candidate URLs
    path('candidates/', CandidateListCreateView.as_view(), name='candidate-list-create'),  # List and create candidates
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),  # Retrieve, update, or delete a specific candidate
    path('associate-resumes/', associate_resumes_with_job, name='associate_resumes_with_job'),
]
