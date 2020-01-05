import os
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import *
from .models import *
from .api import *
from django.core.mail import send_mail
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.conf import settings

def home(request):
    if request.user.is_authenticated:        
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
        else:
            paid = None
    else:
        paid = None
        student = False

    return render(request, 'app/home.html', {'loggedIn': request.user.is_authenticated, 'student': student, 'paid': paid})

def login(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == True):
            paid = None
            return redirect('student-home')
        else:
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            return redirect('restaurant-home')
    else:
        paid = None
        student = False
    return render(request, 'app/login.html', {'loggedIn': request.user.is_authenticated, 'student': student, 'paid': paid})

def logout(request):
    if request.user.is_authenticated:
        return render(request, 'app/logout.html', {'loggedIn': False, 'student': False, 'paid': None})       
    else:
        return redirect('home')
    
def homepage(request):
    if request.user.is_authenticated:       
        if request.user.is_student:           
            return redirect('student-home')
        else:
            return redirect('restaurant-home')
    else:
        return redirect('home')

def register(request):
    if request.user.is_authenticated:        
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
        else:
            paid = None
        return redirect('homepage')
    else:
        paid = None
        student = False
    return render(request, 'app/register.html', {'loggedIn': request.user.is_authenticated, 'student': student, 'paid': paid})

def studentregister(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
        else:
            paid = None
        return redirect('homepage')
    else:
        paid = None
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
        'student': student,
        'paid': paid
    })

def studenthome(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            return redirect('restaurant-home')
        else:
            paid = None
            
            # getting current story postings and corresponding restaurant profiles    
            currentStoryPostings = []
            currentStoryProfiles = []
            for storyPosting in RestaurantStoryPosting.objects.filter(expiry_date__gte=timezone.now(), quantity__gt=0):
                print(storyPosting.description_text)
                print("Now: " + timezone.now().strftime("%m/%d/%Y, %H:%M:%S"))
                print("Expiry Date: " + storyPosting.expiry_date.strftime("%m/%d/%Y, %H:%M:%S"))
                print()
                if not StudentStoryOffer.objects.filter(student=request.user, posting=storyPosting).exists():
                    currentStoryPostings.append(storyPosting)
                    restUser = storyPosting.restaurant
                    currentStoryProfiles.append(RestaurantProfile.objects.get(user=restUser))
            combinedStories = zip(currentStoryPostings, currentStoryProfiles)
            if len(currentStoryPostings) == 0:
                currentStoryPostings = None
                currentStorySubsProfiles = None
                combinedStories = None
            
            # getting current post postings and corresponding restaurant profiles 
            currentPostPostings = []
            currentPostProfiles = []
            for postPosting in RestaurantPostPosting.objects.filter(expiry_date__gte=timezone.now(), quantity__gt=0):
                print(postPosting.description_text)
                print("Now: " + timezone.now().strftime("%m/%d/%Y, %H:%M:%S"))
                print("Expiry Date: " + postPosting.expiry_date.strftime("%m/%d/%Y, %H:%M:%S"))
                print()
                if not StudentPostOffer.objects.filter(student=request.user, posting=postPosting).exists():
                    currentPostPostings.append(postPosting)
                    restUser = postPosting.restaurant
                    currentPostProfiles.append(RestaurantProfile.objects.get(user=restUser))
            combinedPosts = zip(currentPostPostings, currentPostProfiles)          
            if len(currentPostPostings) == 0:
                currentPostPostings = None
                currentPostProfiles = None
                combinedPosts = None
    else:
        paid = None
        student = False
        return redirect('home')

    context = {
        'combinedStories': combinedStories,
        'combinedPosts': combinedPosts,
        'loggedIn': request.user.is_authenticated,
        'user': request.user, 
        'student': student,
        'paid': paid
    }
    return render(request, 'app/studenthome.html', context)

def redeemablerewards(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            return redirect('restaurant-home')
        else:
            paid = None
            
            # getting valid story submission rewards    
            currentStorySubs = []
            if StudentStoryOffer.objects.filter(student=request.user).exists():
                storySubs = StudentStoryOffer.objects.filter(student=request.user)
                currentStorySubsProfiles = []
                currentStoryPostings = []
                for storySub in storySubs:
                    if storySub.posting.expiry_date >= timezone.now() and (not storySub.used) and (not storySub.reported):
                        currentStorySubs.append(storySub)
                        restStoryPosting = storySub.posting
                        currentStoryPostings.append(restStoryPosting)
                        restUser = restStoryPosting.restaurant
                        currentStorySubsProfiles.append(RestaurantProfile.objects.get(user=restUser))
                combinedStories = zip(currentStorySubs, currentStorySubsProfiles, currentStoryPostings)
            if len(currentStorySubs) == 0:
                currentStorySubs = None
                currentStorySubsProfiles = None
                combinedStories = None
            
            # getting valid post submission rewards 
            currentPostSubs = []
            if StudentPostOffer.objects.filter(student=request.user).exists():
                postSubs = StudentPostOffer.objects.filter(student=request.user)
                currentPostSubsProfiles = []
                currentPostPostings = []
                for postSub in postSubs:
                    if postSub.posting.expiry_date >= timezone.now() and (not postSub.used) and (not postSub.reported):
                        currentPostSubs.append(postSub) 
                        restPostPosting = postSub.posting
                        currentPostPostings.append(restPostPosting)
                        restUser = restPostPosting.restaurant
                        currentPostSubsProfiles.append(RestaurantProfile.objects.get(user=restUser))
                combinedPosts = zip(currentPostSubs, currentPostSubsProfiles, currentPostPostings)
            if len(currentPostSubs) == 0:
                currentPostSubs = None
                currentPostSubsProfiles = None
                combinedPosts = None
                
            rewards = (currentStorySubs != None) or (currentPostSubs != None)
    else:
        paid = None
        student = False
        return redirect('home')

    context = {
        'rewards': rewards,
        'combinedStories': combinedStories,
        'combinedPosts': combinedPosts,
        'loggedIn': request.user.is_authenticated, 
        'student': student,
        'paid': paid
    }
    return render(request, 'app/redeemablerewards.html', context)

def redeemstory(request, pk):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            return redirect('restaurant-home')
        else:
            paid = None
            
            # mark indicated reward as being used and re-render redeemable rewards page with new message
            redeemedStory = StudentStoryOffer.objects.get(pk=pk)
            redeemedStory.used = True
            redeemedStory.save()
            
            messages.success(request, f'Your reward has been redeemed!')
            
            # getting valid story submission rewards    
            currentStorySubs = []
            if StudentStoryOffer.objects.filter(student=request.user).exists():
                storySubs = StudentStoryOffer.objects.filter(student=request.user)
                currentStorySubsProfiles = []
                currentStoryPostings = []
                for storySub in storySubs:
                    if storySub.posting.expiry_date >= timezone.now() and (not storySub.used) and (not storySub.reported):
                        currentStorySubs.append(storySub)
                        restStoryPosting = storySub.posting
                        currentStoryPostings.append(restStoryPosting)
                        restUser = restStoryPosting.restaurant
                        currentStorySubsProfiles.append(RestaurantProfile.objects.get(user=restUser))
                combinedStories = zip(currentStorySubs, currentStorySubsProfiles, currentStoryPostings)
            if len(currentStorySubs) == 0:
                currentStorySubs = None
                currentStorySubsProfiles = None
                combinedStories = None
            
            # getting valid post submission rewards 
            currentPostSubs = []
            if StudentPostOffer.objects.filter(student=request.user).exists():
                postSubs = StudentPostOffer.objects.filter(student=request.user)
                currentPostSubsProfiles = []
                currentPostPostings = []
                for postSub in postSubs:
                    if postSub.posting.expiry_date >= timezone.now() and (not postSub.used) and (not postSub.reported):
                        currentPostSubs.append(postSub) 
                        restPostPosting = postSub.posting
                        currentPostPostings.append(restPostPosting)
                        restUser = restPostPosting.restaurant
                        currentPostSubsProfiles.append(RestaurantProfile.objects.get(user=restUser))
                combinedPosts = zip(currentPostSubs, currentPostSubsProfiles, currentPostPostings)
            if len(currentPostSubs) == 0:
                currentPostSubs = None
                currentPostSubsProfiles = None
                combinedPosts = None
    else:
        paid = None
        student = False
        return redirect('home')

    context = {
        'combinedStories': combinedStories,
        'combinedPosts': combinedPosts,
        'loggedIn': request.user.is_authenticated, 
        'student': student,
        'paid': paid
    }
    return render(request, 'app/redeemablerewards.html', context)

def redeempost(request, pk):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            return redirect('restaurant-home')
        else:
            paid = None
            
            # mark indicated reward as being used and re-render redeemable rewards page with new message
            redeemedPost = StudentPostOffer.objects.get(pk=pk)
            redeemedPost.used = True
            redeemedPost.save()
            
            messages.success(request, f'Your reward has been redeemed!')
            
            # getting valid story submission rewards    
            currentStorySubs = []
            if StudentStoryOffer.objects.filter(student=request.user).exists():
                storySubs = StudentStoryOffer.objects.filter(student=request.user)
                currentStorySubsProfiles = []
                for storySub in storySubs:
                    if storySub.posting.expiry_date >= timezone.now() and (not storySub.used) and (not storySub.reported):
                        currentStorySubs.append(storySub)
                        restStoryPosting = storySub.posting
                        restUser = restStoryPosting.restaurant
                        currentStorySubsProfiles.append(RestaurantProfile.objects.get(user=restUser))
                combinedStories = zip(currentStorySubs, currentStorySubsProfiles)
            if len(currentStorySubs) == 0:
                currentStorySubs = None
                currentStorySubsProfiles = None
                combinedStories = None
            
            # getting valid post submission rewards 
            currentPostSubs = []
            if StudentPostOffer.objects.filter(student=request.user).exists():
                postSubs = StudentPostOffer.objects.filter(student=request.user)
                currentPostSubsProfiles = []
                for postSub in postSubs:
                    if postSub.posting.expiry_date >= timezone.now() and (not postSub.used) and (not postSub.reported):
                        currentPostSubs.append(postSub) 
                        restPostPosting = postSub.posting
                        restUser = restPostPosting.restaurant
                        currentPostSubsProfiles.append(RestaurantProfile.objects.get(user=restUser))
                combinedPosts = zip(currentPostSubs, currentPostSubsProfiles)
            if len(currentPostSubs) == 0:
                currentPostSubs = None
                currentPostSubsProfiles = None
                combinedPosts = None
    else:
        paid = None
        student = False
        return redirect('home')

    context = {
        'combinedStories': combinedStories,
        'combinedPosts': combinedPosts,
        'loggedIn': request.user.is_authenticated, 
        'student': student,
        'paid': paid
    }
    return render(request, 'app/redeemablerewards.html', context)    

def submitstory(request, pk):
    if request.user.is_authenticated:       
        if request.user.is_student:  
            if request.method == 'POST':
                story_form = StudentStorySubmission(request.POST, request.FILES, prefix='SS')
                          
                if story_form.is_valid():
                    story = story_form.save(commit=False)
                    link = story_form.cleaned_data.get('link')
                    image = story_form.cleaned_data.get('image')
                    validate = URLValidator()
                    try:
                        validate(link)
                    except ValidationError as e:
                        messages.warning(request, f'Please enter a valid link.')
                        return redirect('student-home')
                    
                    if (link.find("instagram") == -1) :
                        messages.warning(request, f'Please enter a valid Instagram link.')
                        return redirect('student-home')
            
                    if (StudentStoryOffer.objects.filter(link=link).exists()):
                        messages.warning(request, f'This content has been previously submitted.')
                        return redirect('student-home')
                    
                    if (StudentPostOffer.objects.filter(link=link).exists()):
                        messages.warning(request, f'This content has been previously submitted.')
                        return redirect('student-home')
                    
                    story.student = request.user
                    submittedPosting = RestaurantStoryPosting.objects.get(pk=pk)
                    
                    if (submittedPosting.expiry_date < timezone.now()):
                        messages.warning(request, f'This reward has expired.')
                        return redirect('student-home')
                    
                    num = submittedPosting.quantity 
                    submittedPosting.quantity = num-1
                    submittedPosting.save()
                    story.posting = submittedPosting
                    story.save()
                    
                                        
                    messages.success(request, f'Your Instagram story has been submitted and can be found in your redeemable rewards!')
                    return redirect('student-home')
            else:
                story_form = StudentStorySubmission(prefix='SS')

            return render(request, 'app/studentstory.html',{
                'story_form': story_form,
                'loggedIn': request.user.is_authenticated, 
                'student': True,
                'paid': None
            }) 
        else:
            return redirect('restaurant-home')
    else:
        return redirect('home')
    
def submitpost(request, pk):
    if request.user.is_authenticated:       
        if request.user.is_student:  
            if request.method == 'POST':
                post_form = StudentPostSubmission(request.POST, request.FILES, prefix='SP')
                
                if post_form.is_valid():
                    post = post_form.save(commit=False)
                    link = post_form.cleaned_data.get('link')
                    validate = URLValidator()
                    try:
                        validate(link)
                    except ValidationError as e:
                        messages.warning(request, f'Please enter a valid link.')
                        return redirect('student-home')
                    
                    if (link.find("instagram") == -1) :
                        messages.warning(request, f'Please enter a valid Instagram link.')
                        return redirect('student-home')
            
                    if (StudentStoryOffer.objects.filter(link=link).exists()):
                        messages.warning(request, f'This content has been previously submitted.')
                        return redirect('student-home')
                    
                    if (StudentPostOffer.objects.filter(link=link).exists()):
                        messages.warning(request, f'This content has been previously submitted.')
                        return redirect('student-home')
                    
                    
                    post.student = request.user
                    submittedPosting = RestaurantPostPosting.objects.get(pk=pk)
                    
                    if (submittedPosting.expiry_date < timezone.now()):
                        messages.warning(request, f'This reward has expired.')
                        return redirect('student-home')
                    
                    num = submittedPosting.quantity 
                    submittedPosting.quantity = num-1
                    submittedPosting.save()
                    post.posting = submittedPosting
                    post.save()
                    
                    messages.success(request, f'Your Instagram post has been submitted and can be found in your redeemable rewards!')
                    return redirect('student-home')
            else:
                post_form = StudentPostSubmission(prefix='SP')

            return render(request, 'app/studentpost.html',{
                'post_form': post_form,
                'loggedIn': request.user.is_authenticated, 
                'student': True,
                'paid': None
            }) 
        else:
            return redirect('restaurant-home')
    else:
        return redirect('home')

def restaurantregister(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
        else:
            paid = None
        return redirect('homepage')
    else:
        paid = None
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
            send_mail('postento: New Restaurant Payment Verification Needed For User ' + username + '',
                        'Check out the admin portal to follow up with the new restaurant (username: ' + username + '), recieve payment, and change their payment status.',
                        settings.DEFAULT_FROM_EMAIL,
                        [ settings.EMAIL_HOST_USER, 'postentoteam@gmail.com']
            )
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        user_form = RestaurantUserForm(prefix='UF')
        profile_form = RestaurantProfileForm(prefix='PF')

    return render(request, 'app/restaurantregister.html',{
        'r_form': user_form,
        'p_form': profile_form,
        'loggedIn': request.user.is_authenticated, 
        'student': student,
        'paid': paid
    })

def restauranthome(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == True):
            paid = None
            return redirect('student-home')
        else:
            if RestaurantStoryPosting.objects.filter(restaurant=request.user, expiry_date__gte=timezone.now()).exists():
                currentStory = RestaurantStoryPosting.objects.get(restaurant=request.user, expiry_date__gte=timezone.now())
            else:
                currentStory = None
            if RestaurantPostPosting.objects.filter(restaurant=request.user, expiry_date__gte=timezone.now()).exists():
                currentPost = RestaurantPostPosting.objects.get(restaurant=request.user, expiry_date__gte=timezone.now())
            else:
                currentPost = None
            
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
    else:
        paid = None
        return redirect('home')
    
    return render(request, 'app/restauranthome.html', 
                  {'loggedIn': request.user.is_authenticated, 
                   'student': student, 
                   'paid': paid, 
                   'currentStory': currentStory, 
                   'currentPost': currentPost,
                   'user': request.user
                   })

def accountdetails(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == False):
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            restName = restaurantProf.restaurant_name
            paid = restaurantProf.paid
            if not paid:
                return redirect('restaurant-home')
        else:
            paid = None
            return redirect('homepage')
    else:
        paid = None
        student = False

    return render(request, 'app/accountdetails.html',{
        'loggedIn': request.user.is_authenticated, 
        'student': student,
        'paid': paid,
        'restName': restName,
        'user': request.user
    })

def viewsubmissions(request):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == True):
            paid = None
            return redirect('student-home')
        else:
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            if not paid:
                return redirect('restaurant-home')
            
            # get all story submissions
            if RestaurantStoryPosting.objects.filter(restaurant=request.user).exists():
                restStoryPostings = RestaurantStoryPosting.objects.filter(restaurant=request.user)
                storySubs = []
                storyPostings = []
                storyImageUrls = []
                for storyPosting in restStoryPostings:
                    if StudentStoryOffer.objects.filter(posting=storyPosting, reported=False).exists():
                        for storyOffer in StudentStoryOffer.objects.filter(posting=storyPosting, reported=False):
                            storySubs.append(storyOffer)
                            storyPostings.append(storyPosting)
                            storyImageUrls.append(storyOffer.image.url)
                combinedStories = zip(storySubs, storyPostings, storyImageUrls)
            else:
                storySubs = None
                storyPostings = None
                storyImageUrls = None
                combinedStories = None
            if storySubs != None and len(storySubs) == 0:
                combinedStories = None
            
            # get all post submissions
            if RestaurantPostPosting.objects.filter(restaurant=request.user).exists():
                restPostPostings = RestaurantPostPosting.objects.filter(restaurant=request.user)
                postSubs = []
                postPostings = []
                postImageUrls = []
                for postPosting in restPostPostings:
                    if StudentPostOffer.objects.filter(posting=postPosting, reported=False).exists():
                        for postOffer in StudentPostOffer.objects.filter(posting=postPosting, reported=False):
                            postSubs.append(postOffer)
                            postPostings.append(postPosting)
                            postImageUrls.append(postOffer.image.url)
                combinedPosts = zip(postSubs, postPostings, postImageUrls)
            else:
                postSubs = None
                postPostings = None
                postImageUrls = None
                combinedPosts = None
            if postSubs != None and len(postSubs) == 0:
                combinedPosts = None
    else:
        paid = None
        return redirect('home')
    
    return render(request, 'app/viewsubmissions.html', 
                  {'loggedIn': request.user.is_authenticated, 
                   'student': student, 
                   'paid': paid, 
                   'combinedStories': combinedStories, 
                   'combinedPosts': combinedPosts})
    
def restaurantstory(request):
    if request.user.is_authenticated:       
        if request.user.is_student:           
            return redirect('student-home')
        else:
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            if not paid:
                return redirect('restaurant-home')
            
            if request.method == 'POST':
                story_form = RestaurantStoryOffering(request.POST, prefix='RS')

                if story_form.is_valid():
                    restaurantstory = story_form.save(commit=False)
                    restaurantstory.restaurant = request.user
                    restaurantstory.save()
                    messages.success(request, f'Your reward for Instagram stories has been created!')
                    return redirect('restaurant-home')
            else:
                story_form = RestaurantStoryOffering(prefix='RS')

            return render(request, 'app/restaurantstory.html',{
                'story_form': story_form,
                'loggedIn': request.user.is_authenticated, 
                'student': None,
                'paid': paid
            })
    else:
        return redirect('home')
    
def restaurantpost(request):
    if request.user.is_authenticated:       
        if request.user.is_student:           
            return redirect('student-home')
        else:
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            if not paid:
                return redirect('restaurant-home')
            
            if request.method == 'POST':
                post_form = RestaurantPostOffering(request.POST, prefix='RP')

                if post_form.is_valid():
                    restaurantpost = post_form.save(commit=False)
                    restaurantpost.restaurant = request.user
                    restaurantpost.save()
                    messages.success(request, f'Your reward for Instagram posts has been created!')
                    return redirect('restaurant-home')
            else:
                post_form = RestaurantPostOffering(prefix='RP')

            return render(request, 'app/restaurantpost.html',{
                'post_form': post_form,
                'loggedIn': request.user.is_authenticated, 
                'student': None,
                'paid': paid
            })
    else:
        return redirect('home')

def reportstory(request, pk):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == True):
            paid = None
            return redirect('student-home')
        else:
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            if not paid:
                return redirect('restaurant-home')
            
            if request.method == 'POST':
                report_form = ReportStory(request.POST, prefix='RS')
                
                if report_form.is_valid():
                    description_text = report_form.cleaned_data.get('description_text')
                    submittedStory = StudentStoryOffer.objects.get(pk=pk)
                    studentProf = StudentProfile.objects.get(user=submittedStory.student)

                    submittedStory.reported = True
                    submittedStory.save()                    
                    send_mail(
                            'postento: Restaurant user "' + request.user.username + '" has reported Student user "' + studentProf.user.username + '"',
                            'The description of the report reads: "' + description_text + '". Visit the admin portal to modify the student\'s status as needed.',
                            settings.DEFAULT_FROM_EMAIL,
                            [ settings.EMAIL_HOST_USER, 'postentoteam@gmail.com']
                    )
                    print('postento: Restaurant user "' + request.user.username + '" has reported Student user "' + studentProf.user.username + '" for student\'s posting posting pk =' + str(submittedStory.pk))
                    print('The description of the report reads: "' + description_text + '". Visit the admin portal to modify the student\'s status as needed.')
                    messages.success(request, f'Your report has been recieved and it will be reviewed. In the meantime, we\'ve removed the reported submission.')
                    return redirect('view-submissions')
            else:
                report_form = ReportStory(prefix='RS')

            return render(request, 'app/reportstory.html',{
                'report_form': report_form,
                'loggedIn': request.user.is_authenticated, 
                'student': False,
                'paid': None
            }) 
    else:
        paid = None
        return redirect('home')
    
def reportpost(request, pk):
    if request.user.is_authenticated:
        student = request.user.is_student
        if (student == True):
            paid = None
            return redirect('student-home')
        else:
            restaurantProf = RestaurantProfile.objects.get(user=request.user)
            paid = restaurantProf.paid
            if not paid:
                return redirect('restaurant-home')
            
            if request.method == 'POST':
                report_form = ReportPost(request.POST, prefix='RP')
                
                if report_form.is_valid():
                    description_text = report_form.cleaned_data.get('description_text')
                    submittedPost = StudentPostOffer.objects.get(pk=pk)
                    studentProf = StudentProfile.objects.get(user=submittedPost.student)
                    
                    submittedPost.reported = True
                    submittedPost.save()  
                    
                    send_mail(
                            'postento: Restaurant user "' + request.user.username + '" has reported Student user "' + studentProf.user.username + '"',
                            'The description of the report reads: "' + description_text + '". Visit the admin portal to modify the student\'s status as needed.',
                            settings.DEFAULT_FROM_EMAIL,
                            [ settings.EMAIL_HOST_USER, 'postentoteam@gmail.com']
                    )
                    print('postento: Restaurant user "' + request.user.username + '" has reported Student user "' + studentProf.user.username + '" for student\'s posting posting pk =' + str(submittedPost.pk))
                    print('The description of the report reads: "' + description_text + '". Visit the admin portal to modify the student\'s status as needed.')
                    messages.success(request, f'Your report has been recieved and it will be reviewed. In the meantime, we\'ve removed the reported submission.')
                    return redirect('view-submissions')
            else:
                report_form = ReportPost(prefix='RP')

            return render(request, 'app/reportpost.html',{
                'report_form': report_form,
                'loggedIn': request.user.is_authenticated, 
                'student': False,
                'paid': None
            }) 
    else:
        paid = None
        return redirect('home')