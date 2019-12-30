from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)

admin.site.register(StudentProfile)

admin.site.register(RestaurantProfile)

admin.site.register(RestaurantPostPosting)

admin.site.register(RestaurantStoryPosting)

admin.site.register(StudentPostOffer)

admin.site.register(StudentStoryOffer)

