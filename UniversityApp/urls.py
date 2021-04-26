"""UniversityApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include # for auth
from django.views.generic.base import TemplateView # new
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
    path('accounts/', include('django.contrib.auth.urls')), # new
    path('admin/', views.administrator, name='admin'),
    path('student/', views.student, name='student'),
    path('student/studentResult/', views.studentResult),
    path('professor/', views.professor, name='professor'),
    path('professor/courses/', views.professorCourses),
    path('professor/students/', views.professorStudents),
    path('admin/f1/', views.f1),
    path('admin/f2/', views.f2),
    path('admin/f3/', views.f3),
    ]
