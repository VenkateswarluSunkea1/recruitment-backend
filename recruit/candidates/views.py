# candidates/views.py

from rest_framework import generics
from .models import Candidate, Job
from .serializers import CandidateSerializer, JobSerializer

# List all jobs and create a new job
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# Retrieve, update, or delete a specific job
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# List all candidates and create a new candidate
class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

# Retrieve, update, or delete a specific candidate
class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
