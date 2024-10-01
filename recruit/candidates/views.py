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
    
@api_view(['GET'])
def getAllResumes(request):
    print('enteressdfsdfsdf')
    try:
        # Fetch all resumes from the database
        resumes = Resume.objects.all()

        # Serialize the data
        serializer = ResumeSerializer(resumes, many=True)
        print(serializer.data,'sdfbshfbshdfsdf')
        # Return the serialized data with a success message
        return Response({"success": "Resumes retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)

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
