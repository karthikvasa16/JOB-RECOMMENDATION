# AI Job Portal

## Overview
AI Job Portal is a Django-based web application designed to streamline job searching and recruitment. It offers features such as job listings, resume screening with AI-based matching, job recommendations, web scraping for external job postings, and job distribution visualization.

## Features
- **User Authentication**: Secure login, registration, and profile management.
- **Job Listings**: Browse and filter available jobs with unique location-based filtering.
- **Resume Screening**: AI-powered resume screening using TF-IDF and cosine similarity.
- **Job Recommendations**: Personalized job recommendations based on uploaded resumes.
- **Web Scraping**: Fetch job postings from external job portals using an API.
- **Job Distribution Graphs**: Visualize job availability using Matplotlib and Seaborn.
- **Notifications**: Automatic alerts for job matches.

## Technology Stack
- **Backend**: Django (Python)
- **Database**: SQLite3
- **Machine Learning**: Scikit-learn (TF-IDF & Cosine Similarity)
- **Web Scraping**: Requests API
- **Visualization**: Matplotlib, Seaborn
- **File Processing**: PyMuPDF (PDF), docx2txt (DOCX)
- **Frontend**: HTML, CSS, Bootstrap

## Installation & Setup
### Prerequisites
- Python 3.8+
- Virtual environment setup (optional but recommended)

### Steps to Run Locally
1. **Clone the repository**
   ```sh
   git clone https://github.com/your-repository/ai-job-portal.git
   cd ai-job-portal
   ```
2. **Create and activate a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations and start the server**
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```
5. **Access the application** at `http://127.0.0.1:8000/`

## Usage
- **Job Seekers**:
  - Register and upload a resume.
  - Browse and apply for jobs.
  - Receive AI-driven job recommendations.
- **Employers**:
  - Post job openings.
  - View job applications.
- **Admin Panel**:
  - Manage users, jobs, and notifications.



