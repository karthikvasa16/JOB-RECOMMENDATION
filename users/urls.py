from django.urls import path
from . import views
urlpatterns = [
    path('register-applicant/', views.register_applicant, name = 'register-applicant'),
    path('register-recruiter/', views.register_recruiter, name = 'register-recruiter'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('delete-user/', views.delete_user, name = 'delete-user'),
    path('verify-user/<str:pk>', views.verify_user, name = 'verify-user'),
]