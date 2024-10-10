from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    CandidateListCreateView,
    CandidateDetailView,
    ResumeUploadView,
    getAllResumes,
    associate_resumes_with_job,
    get_jobs_by_resume,
    job_list_view,
)

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('resumes/', getAllResumes, name='resume-list'), 
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'), 

    # Candidate URLs
    path('candidates/', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('associate-resumes/', associate_resumes_with_job, name='associate_resumes_with_job'),
    path('resumes/<int:resume_id>/jobs/', get_jobs_by_resume, name='get-jobs-by-resume'),
    path('get-jobs-by-ids/', job_list_view, name='job-list'),
]
