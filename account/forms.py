from typing import Any
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import TextInput, PasswordInput

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile

from library.models import Category


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if(User.objects.filter(email = email).exists()):
            raise forms.ValidationError("Email already in used")
        
        if len(email) >= 300:
            raise forms.ValidationError("Your email is too long")
        
        return email

class LoginForm(AuthenticationForm):

    #can only login with username and password, not email and password
    username = forms.CharField(widget = TextInput())
    password = forms.CharField(widget = PasswordInput())

class UpdateUserForm(forms.ModelForm):
    password =  None

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        exclude = ["password1", "password2"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if(User.objects.filter(email = email).exclude(pk = self.instance.pk).exists()):
            raise forms.ValidationError("Email already in used")
        
        if len(email) >= 300:
            raise forms.ValidationError("Your email is too long")
        
        return email

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["city", "country", "about_me", "liked_categories"]

    city = forms.CharField()
    about_me = forms.DateInput()

    liked_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic"]

    profile_pic = forms.ImageField(widget = forms.FileInput(attrs = {'class': 'form-control-file'}))

