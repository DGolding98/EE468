from django.shortcuts import render
import mysql.connector
from django.contrib.auth import authenticate, login

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Instructor 

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...

# def index(request):
  
  # template = loader.get_template('myapp/form.html')
  # context = { }

  # return HttpResponse(template.render(context, request))


# def show(request):
  
  # amount=request.POST['amount']
  # print(amount)

  # data = Instructor.objects.filter(salary__gt=amount)
  # for r in data:
     # print(r)
  # template = loader.get_template('myapp/table.html')
  # context = {
        # 'rows': data,
    # }

  # return HttpResponse(template.render(context, request))
