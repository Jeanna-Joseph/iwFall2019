from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    is_student = models.BooleanField(default=True)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='student_profile')
    instagram_handle = models.CharField(max_length=30, blank=True)

class RestaurantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='restaurant_profile')
    restaurant_name = models.CharField(max_length=60, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # print('****', created)
    if instance.is_student:
        StudentProfile.objects.get_or_create(user = instance)
    else:
        RestaurantProfile.objects.get_or_create(user = instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # print('_-----')	
    if instance.is_student:
        instance.student_profile.save()
    else:
        instance.restaurant_profile.save()

class RestaurantPostPosting(models.Model):
    description_text = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0) 
    pub_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(default=timezone.now()+timezone.timedelta(days=30))
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE)

class RestaurantStoryPosting(models.Model):
    description_text = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(default=timezone.now()+timezone.timedelta(days=30))
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE)

class StudentPostOffer(models.Model):
    posting = models.ForeignKey(RestaurantPostPosting, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)
    acquired_date = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

class StudentStoryOffer(models.Model):
    posting = models.ForeignKey(RestaurantStoryPosting, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)
    acquired_date = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(User, on_delete=models.CASCADE)