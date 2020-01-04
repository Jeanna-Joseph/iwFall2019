#import os
#from django.shortcuts import render, redirect, render_to_response
#from django.http import HttpResponse
#from django.contrib import messages
#from django.contrib.auth.decorators import login_required
#from .forms import *
from .models import *
#from django.conf import settings


# Create your views here.                                                                                                 
def getPostPostings(rest):
    return RestaurantPostPosting.objects.filter(restaurant=rest)

def getIsPaid(rest):
    restaurantProf = RestaurantProfile.objects.get(user=rest)
    return restaurantProf.paid