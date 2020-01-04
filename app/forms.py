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
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'validate',}))
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

class StudentPostSubmission(forms.ModelForm):
    link = forms.CharField(
        max_length=200,
        widget=forms.Textarea(),
        help_text='Paste a link to your post here.'
    )
    class Meta:
        model = StudentPostOffer
        fields = ('link',)
    def clean(self):
        cleaned_data = super(StudentPostSubmission, self).clean()
        link = cleaned_data.get('link')
        if not link:
            raise forms.ValidationError('Link required')

class StudentStorySubmission(forms.ModelForm):
    link = forms.CharField(
        max_length=200,
        widget=forms.Textarea(),
        help_text='Paste a link to your story here.'
    )
    class Meta:
        model = StudentStoryOffer
        fields = ('link',)
    def clean(self):
        cleaned_data = super(StudentStorySubmission, self).clean()
        link = cleaned_data.get('link')
        if not link:
            raise forms.ValidationError('Link required')

class RestaurantPostOffering(forms.ModelForm):
    description_text = forms.CharField(max_length=200, required=True, help_text='Required: enter a description of the reward.')
    class Meta:
        model = RestaurantPostPosting
        fields = ('description_text',)
    def clean(self):
        cleaned_data = super(RestaurantPostOffering, self).clean()
        description_text = cleaned_data.get('description_text')
        if not description_text:
            raise forms.ValidationError('Description of reward required')

class RestaurantStoryOffering(forms.ModelForm):
    description_text = forms.CharField(max_length=200, required=True, help_text='Required: enter a description of the reward.')
    class Meta:
        model = RestaurantStoryPosting
        fields = ('description_text',)
    def clean(self):
        cleaned_data = super(RestaurantStoryOffering, self).clean()
        description_text = cleaned_data.get('description_text')
        if not description_text:
            raise forms.ValidationError('Description of reward required')
