from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

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
