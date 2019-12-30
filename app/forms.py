from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import get_user_model
 
class StudentUserForm(UserCreationForm):    
    instagram_handle = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'instagram_handle', 'email', 'username', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user
        
class RestaurantUserForm(UserCreationForm):  
    restaurant_name = forms.CharField(max_length=60, required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'restaurant_name', 'email', 'username', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = False
        if commit:
            user.save()
        return user
 
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('instagram_handle',)
        
class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantProfile
        fields = ('restaurant_name',)

class StudentPostSubmission(forms.Form):
    link = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Paste a link to your post here.'
    )
    def clean(self):
        cleaned_data = super(StudentPostSubmission, self).clean()
        message = cleaned_data.get('link')
        if not name and not email and not message:
            raise forms.ValidationError('Link required')

class StudentStorySubmission(forms.Form):
    link = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Paste a link to your story here.'
    )
    def clean(self):
        cleaned_data = super(StudentStorySubmission, self).clean()
        link = cleaned_data.get('link')
        if not link:
            raise forms.ValidationError('Link required')

class RestaurantPostOffering(forms.Form):
    description_text = forms.CharField(max_length=200, required=True, help_text='Required: enter a description of the reward.')
    quantity = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(RestaurantPostOffering, self).clean()
        description_text = cleaned_data.get('description_text')
        quantity = cleaned_data.get('quantity')
        if not quantity or not description_text:
            raise forms.ValidationError('Fill out all required fields')

class RestaurantStoryOffering(forms.Form):
    description_text = forms.CharField(max_length=200, required=True, help_text='Required: enter a description of the reward.')
    quantity = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(RestaurantStoryOffering, self).clean()
        description_text = cleaned_data.get('description_text')
        quantity = cleaned_data.get('quantity')
        if not quantity or not description_text:
            raise forms.ValidationError('Fill out all required fields')
