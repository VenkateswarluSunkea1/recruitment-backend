from rest_framework import generics
from rest_framework.response import Response
from .models import Resume,Job
from .serializers import ResumeSerializer, JobSerializer
import docx
import PyPDF2
import io
import re
import spacy
from spacy.tokens import DocBin
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import json
from django.shortcuts import get_object_or_404

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

class ResumeUploadView(generics.CreateAPIView):
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        
        # Check the file type and extract text accordingly
        text = ''
        if file.name.endswith('.docx'):
            # Process .docx file
            doc = docx.Document(file)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file.name.endswith('.pdf'):
            # Process .pdf file
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            print(pdf_reader,'pdf_readersf')
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
        else:
            return Response({"error": "Unsupported file type"}, status=400)

        # Extract details from the extracted text
        name = self.extract_name(text)
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        skills = self.extract_skills(text)

        # Save to database
        resume = Resume.objects.create(
            name=name,
            email=email,
            phone=phone,
            skills=skills,
            file=file
        )
        
        serializer = self.get_serializer(resume)
        return Response(serializer.data)

    def extract_name(self, text):
        # Attempt to extract name from the text (assuming it's the first line)
        lines = text.splitlines()
        if lines:
            name = lines[0].strip()  # Assuming the name is the first line
            return name
        return "Name not found"

    def extract_email(self, text):
        # Regex pattern for email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        if match:
            return match.group(0)  # Return the first matched email
        return "Email not found"

    def extract_phone(self, text):
        # Regex pattern for phone numbers (adjust as needed for your use case)
        phone_pattern = r'\b\d{10}\b|\+\d{1,3}\s?\d{10}|\(\d{3}\)\s?\d{3}-?\d{4}'
        match = re.search(phone_pattern, text)
        if match:
            return match.group(0)  # Return the first matched phone number
        return "Phone number not found"

    def extract_skills(self, text):
        # Example skills extraction; this can be tailored as needed
        skills_keywords = ['Python', 'Django', 'JavaScript', 'React', 'Node.js', 'SQL', 'Machine Learning', 'CSS', 'HTML']
        skills_found = [skill for skill in skills_keywords if skill.lower() in text.lower()]

        if skills_found:
            return ', '.join(skills_found)
        return "Skills not found"
    
# @api_view(['GET'])
# def getAllResumes(request):
#     print('enteressdfsdfsdf')
#     try:
#         # Fetch all resumes from the database
#         resumes = Resume.objects.all()

#         # Serialize the data
#         serializer = ResumeSerializer(resumes, many=True)
#         print(serializer.data,'sdfbshfbshdfsdf')
#         # Return the serialized data with a success message
#         return Response({"success": "Resumes retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)

#     except Exception as e:
#         error_message = f"API error: {e}"
#         return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResumePagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'limit'  # Parameter for the client to specify page size
    max_page_size = 100  # Maximum limit of items per page

@api_view(['GET'])
def getAllResumes(request):
    print('API endpoint hit',request.query_params.get('skill set'))
    try:
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
        offset = (page - 1) * limit
        
        # Fetch resumes with pagination
        # resumes = Resume.objects.all()[offset:offset + limit]
        resumes = Resume.objects.all()

        # Filtering logic based on active filters
        skill_set_filter = request.query_params.get('skill set')
        print(skill_set_filter,'skill_set_filterasdasd')
        if skill_set_filter:
            skill_set_filter = json.loads(skill_set_filter)
            option = skill_set_filter.get('option')
            print('entered2')
            value = skill_set_filter.get('value')
            print(option,value,'optionassd')
            if option == "contains":
                resumes = resumes.filter(skills__icontains=value)
            elif option == "not_contains":
                resumes = resumes.exclude(skills__icontains=value)
            elif option == "is":
                resumes = resumes.filter(skills=value)
            elif option == "is_not":
                resumes = resumes.exclude(skills=value)
            elif option == "starts_with":
                resumes = resumes.filter(skills__startswith=value)
            elif option == "ends_with":
                resumes = resumes.filter(skills__endswith=value)
            elif option == "is_empty":
                resumes = resumes.filter(skills__isnull=True)  # Assuming skills is nullable
            elif option == "is_not_empty":
                resumes = resumes.exclude(skills__isnull=True)
        
        total_count = len(resumes)
        # Paginate the results
        resumes = resumes[offset:offset + limit]
        print(resumes,'rsusfnsdfsdf')
        # Serialize the data
        serializer = ResumeSerializer(resumes, many=True)

        # Count total resumes for pagination info
        # total_count = Resume.objects.count()
        print(total_count,'total_countdbfsdf')
        # Return the serialized data with total count
        return Response({
            'total_count': total_count,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        error_message = f"API error: {e}"
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get(self, request, job_id):
    try:
        # Get the job based on the job_id
        job = Job.objects.get(id=job_id)
        job_description = job.description.lower()
        
        # Split job description into keywords
        job_keywords = set(job_description.split())

        # Filter candidates whose skills match job description keywords
        matching_candidates = Resume.objects.filter(
            Q(skills__icontains=job.description) |
            Q(experience_in_years__gte=2)  # Example: filter by minimum experience
        )
        
        # Return the matching candidates
        candidates_data = [
            {
                "name": candidate.name,
                "email": candidate.email,
                "phone": candidate.phone,
                "skills": candidate.skills,
                "experience": candidate.experience_in_years,
                "current_employer": candidate.current_employer
            }
            for candidate in matching_candidates
        ]
        return Response(candidates_data)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

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
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
# Retrieve, update, or delete a specific candidate
class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

@api_view(['POST'])
def associate_resumes_with_job(request):
    # Parse the request body to get the job_id and selected resume_ids
    data = json.loads(request.body)
    job_id = data.get('job_id')
    resume_ids = data.get('resume_ids', [])

    # Get the Job instance by id
    job = get_object_or_404(Job, id=job_id)

    # Get the Resume instances by ids and associate them with the job
    resumes = Resume.objects.filter(id__in=resume_ids)

    # Add job to each resume
    for resume in resumes:
        resume.jobs.add(job)
    print(resumes,'resumessdfsfsfw')
    return Response({"message": "Resumes associated successfully"}, status=200)