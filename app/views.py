from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.                                                                                                 
def home(request):
    if request.user.is_authenticated:        
        student = request.user.is_student
    else:
        student = False

    return render(request, 'app/home.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def studenthome(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            return redirect('restaurant-home')
    else:
        student = False
        return redirect('home')

    context = {
        'postPostings': RestaurantPostPosting.objects.all(),
        'storyPostings': RestaurantStoryPosting.objects.all(),
        'loggedIn': request.user.is_authenticated, 
        'student': student
    }

    return render(request, 'app/studenthome.html', context)

def register(request):
    if request.user.is_authenticated:        
        student = request.user.is_student
        return redirect('homepage')
    else:
        student = False
    return render(request, 'app/register.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def studentregister(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        return redirect('homepage')
    else:
        student = False

    if request.method == 'POST':
        user_form = StudentUserForm(request.POST, prefix='UF')
        profile_form = StudentProfileForm(request.POST, prefix='PF')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            user.student_profile.instagram_handle = user_form.cleaned_data.get('instagram_handle')
            user.student_profile.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        user_form = StudentUserForm(prefix='UF')
        profile_form = StudentProfileForm(prefix='PF')

    return render(request, 'app/studentregister.html',{
        'r_form': user_form,
        'p_form': profile_form,
        'loggedIn': request.user.is_authenticated, 
        'student': student
    })

def restaurantregister(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        return redirect('homepage')
    else:
        student = False

    if request.method == 'POST':
        user_form = RestaurantUserForm(request.POST, prefix='UF')
        profile_form = RestaurantProfileForm(request.POST, prefix='PF')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            user.restaurant_profile.restaurant_name = user_form.cleaned_data.get('restaurant_name')
            user.restaurant_profile.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        user_form = RestaurantUserForm(prefix='UF')
        profile_form = RestaurantProfileForm(prefix='PF')

    return render(request, 'app/restaurantregister.html',{
        'r_form': user_form,
        'p_form': profile_form,
        'loggedIn': request.user.is_authenticated, 
        'student': student
    })

def login(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == True):
            return redirect('student-home')
        else:
            return redirect('restaurant-home')
    else:
        student = False
    return render(request, 'app/login.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def homepage(request):
    if request.user.is_authenticated:       
        if request.user.is_student:           
            return redirect('student-home')
        else:
            return redirect('restaurant-home')

def restauranthome(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == True):
            return redirect('student-home')
    else:
        return redirect('home')
    
    return render(request, 'app/restauranthome.html', {'loggedIn': request.user.is_authenticated, 'student': student})

def logout(request):
    if request.user.is_authenticated:
        return render(request, 'app/logout.html', {'loggedIn': False, 'student': False})       
    else:
        return redirect('home')
    
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