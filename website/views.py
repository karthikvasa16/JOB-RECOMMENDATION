from django.shortcuts import render
from django.db.models import Count
from job.models import Job, ApplyJob, Resume
from .filter import Jobfilter
import requests
from django.http import HttpResponse
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.db import connection 
import matplotlib.pyplot as plt
from resume.models import Resume
def home(request):
    filter = Jobfilter(request.GET, queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context = {'filter': filter}
    return render(request, 'website/home.html', context)

def job_details(request, pk):
    job = Job.objects.get(pk=pk)
    has_applied = ApplyJob.objects.filter(user=request.user, job=pk).exists() if request.user.is_authenticated and request.user.is_applicant and request.user.is_verified else False
    context = {'job': job, 'has_applied': has_applied}
    return render(request, 'website/job_details.html', context)

def fetch_jobs(search_term, location):
    url = "https://jobs-search-api.p.rapidapi.com/getjobs"

    payload = {
        "search_term": search_term,
        "location": location,
        "results_wanted": 20,
        "site_name": ["indeed", "linkedin", "zip_recruiter", "glassdoor"],
        "distance": 50,
        "job_type": "fulltime",
        "is_remote": False,
        "linkedin_fetch_description": False,
        "hours_old": 48
    }

    headers = {
        "x-rapidapi-key": "e980a51c0dmshfee51235fc71445p1e7438jsnffd9be124e8b",
        "x-rapidapi-host": "jobs-search-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("jobs", [])
    else:
        return []

def web_scraping(request):
    jobs = []
    search_term = request.GET.get("search_term", "")
    location = request.GET.get("location", "")

    if search_term and location:
        jobs = fetch_jobs(search_term, location)

    return render(request, "website/scraping.html", {"jobs": jobs, "search_term": search_term, "location": location})

def job_listing(request):
    """Display job listings with unique location filter."""
    jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
    locations = Job.objects.values_list('city', flat=True).distinct()  # Unique locations

    location = request.GET.get("location", "")
    if location:
        jobs = jobs.filter(city__iexact=location)  # Filter by selected location
    """Recommend jobs where Job.title matches Resume.title."""
    recommended_jobs = []

    if request.user.is_authenticated:

        user_resume = Resume.objects.filter(user_id=request.user.id).first()  # Get the user's resume
        
        if user_resume:
            # Find jobs where Job.title matches Resume.title
            recommended_jobs = Job.objects.filter(title=user_resume.title, is_available=True)

    
    context = {'jobs': jobs, 'locations': locations, 'location': location, 'recommended_jobs': recommended_jobs, 'title':user_resume.title}
    return render(request, 'website/job_listing.html', context)

def job_graph(request):
    """Generate job distribution graph dynamically based on selected location."""
    location = request.GET.get("location", "")

    # Filter jobs by selected location
    jobs = Job.objects.filter(is_available=True)
    if location:
        jobs = jobs.filter(city__iexact=location)

    # Count job occurrences by title
    job_counts = jobs.values("title").annotate(count=Count("title")).order_by("-count")

    if not job_counts:
        return HttpResponse("No jobs available for this location.", content_type="text/plain")

    # Generate the graph with a smaller size
    plt.figure(figsize=(4, 3))  # 📏 Reduced size
    sns.barplot(y=[job["title"] for job in job_counts], x=[job["count"] for job in job_counts], palette="coolwarm")
    plt.xlabel("Jobs")
    plt.ylabel("Titles")
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(f"{location}" if location else "Job Distribution", fontsize=10)

    # Render the plot as an HTTP response
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type="image/png")