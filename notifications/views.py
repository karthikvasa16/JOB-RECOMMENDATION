import fitz  # PyMuPDF for PDF text extraction
import docx2txt
import nltk
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import User, Notif
from job.models import Job, Resume

nltk.download('stopwords')
from nltk.corpus import stopwords

# Function to extract text from resumes (PDF or DOCX)
def extract_text_from_resume(file):
    text = ""
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    return text

# Function to preprocess text (remove stopwords, lowercase, etc.)
def preprocess_text(text):
    stop_words = set(stopwords.words("english"))
    words = text.lower().split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# Function to screen resumes against job descriptions and prevent duplicate notifications
def screen_resumes():
    resumes = Resume.objects.all()  
    jobs = Job.objects.all()  

    for resume in resumes:
        resume_text = extract_text_from_resume(resume.upload_resume)
        processed_resume = preprocess_text(resume_text)

        for job in jobs:
            job_description = f"{job.title} {job.requirements} {job.ideal_candidate}"
            processed_job_desc = preprocess_text(job_description)

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([processed_resume, processed_job_desc])
            similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

            if similarity_score > 0.10:
                # Check if a notification already exists for this user and job
                existing_notif = Notif.objects.filter(
                    user=resume.user,
                    content__icontains=f"'{job.title}'"
                ).exists()

                if not existing_notif:
                    Notif.objects.create(
                        user=resume.user,
                        content=f"Your resume matches the job '{job.title}'",
                    )


# View for displaying notifications
def notifications(request):
    if request.user.is_authenticated and request.user.is_verified:
        # Run resume screening only if no notifications exist for the user
        if not Notif.objects.filter(user=request.user).exists():
            screen_resumes()

        notifs = Notif.objects.filter(user=request.user).order_by('-timestamp')
        context = {'notifs': notifs, 'user': request.user}
        return render(request, 'notifications/notifications.html', context)
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')

# View for deleting a notification
def delete_notification(request, pk):
    if request.user.is_authenticated and request.user.is_verified:
        notif = Notif.objects.filter(user=request.user, pk=pk).first()
        if notif:
            notif.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'Permission Denied')
        return redirect('dashboard')
