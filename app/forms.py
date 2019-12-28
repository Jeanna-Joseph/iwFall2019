from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
 
class StudentRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Required: enter first and last name.')
    instagram_handle = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    student_status = forms.BooleanField(widget=forms.HiddenInput(), initial=True) 

    class Meta:
        model = User
        fields = ['username', 'name', 'instagram_handle', 'email', 'password1', 'password2', 'student_status']


class RestaurantRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Required: enter name of restaurant.')
    instagram_handle = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)
    student_status = forms.BooleanField(widget=forms.HiddenInput(), initial=False) 
    class Meta:
        model = User
        fields = ['username', 'name', 'instagram_handle', 'email', 'password1', 'password2', 'student_status']


class ProfileForm(forms.ModelForm):
    is_student = forms.BooleanField()

    class Meta:
        model = Profile
        fields = ['is_student']
        
    def set_is_student(self, status):
        data = self.data.copy()
        data['is_student'] = status
        self.data = data

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
