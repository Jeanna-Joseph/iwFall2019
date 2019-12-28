from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.                                                                                                 
def home(request):
    if request.user.is_authenticated:        
        student = request.user.profile.is_student
    else:
        student = False

    return render(request, 'app/home.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def studenthome(request):
    if request.user.is_authenticated:
        student = request.user.profile.is_student
    else:
        student = False

    context = {
        'postPostings': RestaurantPostPosting.objects.all(),
        'storyPostings': RestaurantStoryPosting.objects.all(),
        'loggedIn': request.user.is_authenticated, 
        'student': student
    }

    return render(request, 'app/studenthome.html', context)

def register(request):
    #if 'loggedIn' in request.GET:
    #    loggedIn = request.GET['loggedIn']
    #else:
    #    loggedIn = False
    #if 'student' in request.GET:
    #    student = request.GET['student']
    #else:
    #    student = False
    if request.user.is_authenticated:
        student = request.user.profile.is_student
    else:
        student = 0

    return render(request, 'app/register.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def studentregister(request):
    #if 'loggedIn' in request.GET:
    #    loggedIn = request.GET['loggedIn']
    #else:
    #    loggedIn = False
    #if 'student' in request.GET:
    #    student = request.GET['student']
    #else:
    #    student = False
   if request.user.is_authenticated:
       student = request.user.profile.is_student
   else:
       student = 0

   if request.method == 'POST':
       r_form = StudentRegisterForm(request.POST)
       
       if r_form.is_valid():
           r_form.save()
           p_form = ProfileForm(request.POST)
           p_form.set_is_student(1)
           if p_form.is_valid():
               p_form.save()
           username = r_form.cleaned_data.get('username')
           messages.success(request, f'Account created for {username}')
           return redirect('login')
   else:
       r_form = StudentRegisterForm()
   return render(request, 'app/studentregister.html', {'r_form': r_form, 'loggedIn': request.user.is_authenticated, 'student': student})

def restaurantregister(request):
    if request.user.is_authenticated:
        student = request.user.profile.is_student
    else:
        student = 0
    
    if request.method == 'POST':
        r_form = RestaurantRegisterForm(request.POST)

        if r_form.is_valid():
            r_form.save()
            p_form = ProfileForm(request.POST)
            p_form['is_student'].initial = 0
            if p_form.is_valid():
                p_form.save()
            username = r_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        r_form = RestaurantRegisterForm()
    return render(request, 'app/restaurantregister.html', {'r_form': r_form, 'loggedIn': request.user.is_authenticated, 'student': student})

def login(request):
    if request.user.is_authenticated:
        student = request.user.profile.is_student
    else:
        student = 0

    return render(request, 'app/login.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def studentlogin(request):
    if request.user.is_authenticated:
        student = request.user.profile.is_student
    else:
        student = 0
    return render(request, 'app/studentlogin.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def restaurantlogin(request):
    if request.user.is_authenticated:
        student = request.user.profile.is_student
    else:
        student = 0
    return render(request, 'app/restaurantlogin.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def homepage(request):
    if request.user.is_authenticated:       
        if request.user.student_status:           
            return redirect('student-home')
        else:
            return redirect('restaurant-home')

def restauranthome(request):
    if request.user.is_authenticated:
        student = request.user.profile.is_student
    else:
        student = 0
    
    return render(request, 'app/restauranthome.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def logout(request):
    return render(request, 'app/logout.html', {'loggedIn': 0, 'student': 0})

#def studentsubmission(request):
#    if request.method == 'POST':
        #if:
#        form = StudentPostSubmission(request.POST)
        #else:
        #    form = StudentStorySubmission(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('restaurant-home')
#    else:
        #if:
    #        form = StudentPostSubmission(request.POST)
       # else:
        #    form = StudentStorySubmission(request.POST)
#    return render(request, 'app/studentsubmission.html', {'form': form, 'loggedIn': request.user.is_authenticated, 'student': student})

#def restaurantsubmission(request):
#    if request.method == 'POST':
#        if:
#        form = RestaurantPostOffering(request.POST)
 #       else:
  #          form = RestaurantStoryOffering(request.POST)
 #       if form.is_valid():
  #          form.save()
   #         return redirect('restaurant-home')
  #  else:
       #  if:
   #     form = RestaurantPostOffering(request.POST)
        #else:
        #    form = RestaurantStoryOffering(request.POST)
   # return render(request, 'app/restaurantsubmission.html', {'form': form, 'loggedIn': request.user.is_authenticated, 'student': student})
