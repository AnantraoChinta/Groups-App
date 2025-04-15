from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from base.decorators import not_registered
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm
from django.http import HttpResponse
from django.contrib import messages

import sys
import re

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    # if request.method == 'POST':
    #     username = request.POST.get('username').lower()
    #     password = request.POST.get('password')
    #     accountType = request.POST.get('auth')
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'Username or Password does not exist')

    return render(request, 'registration/login.html')

 

def logoutUser(request):
    logout(request)
    return redirect('login')

# Precondition: Form will only be be valid if the email consists of an FRHSD email,
                # which is can be verified with the Gmail API to determine the FRHSD email actually exists

@not_registered
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         email = request.POST.get('email').lower()
    #         # If the first three characters of the email are numbers, the user is a student
    #         if email[0:3].isnumeric():
    #             group = Group.objects.get(name="student")
    #         # Otherwise, the user is a teacher
    #         else:
    #             group = Group.objects.get(name="teacher")
    #             print("this is teacher")

    #         user.groups.add(group)
            
    #         login(request, user)
    #         return redirect('home')
    # else:
    #     # form object now has the validation errors if it did not validate
    #     form = UserRegistrationForm()
    
    
    context = {}

    return render(request, 'registration/register.html', context)


    
