from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, UpdateUserForm, ProfileForm, ProfilePicForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Profile

from review.models import Review

from library.models import Book

from django.contrib import messages

from django.db.models import Avg, OuterRef, Subquery, Count, Case, When, Q, F


# Create your views here.


def sign_up(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()

            Profile.objects.create(user = user)

            return redirect("login")

    context = {'form': form}

    return render(request, 'account/registration/sign-up.html', context)

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)

        if form.is_valid():

            print("in here")

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth.login(request, user)

                return redirect("my-books", shelf_option = "all" )
            
    context = {'form': form}

    return render(request, 'account/login.html', context)

def user_logout(request):
    auth.logout(request)

    return redirect("library")

@login_required(login_url = 'login')

def dashboard(request):

    account_form = UpdateUserForm(instance = request.user)

    user_profile = Profile.objects.get(user = request.user)

    profile_form = ProfileForm(instance = user_profile)
    profile_pic_form = ProfilePicForm(instance = user_profile)

    if(request.method == 'POST'):
        if('account' in request.POST):
            account_form = UpdateUserForm(request.POST, instance = request.user)

            if account_form.is_valid():
                account_form.save()
            
            messages.success(request, "Account Updated!")

            return redirect("dashboard")

        elif('personal' in request.POST):

            profile_form = ProfileForm(request.POST, instance = user_profile)

            if profile_form.is_valid():
                profile_form.save()

            messages.success(request, "Personal Info Updated!")

            return redirect("dashboard")
        
        elif ('profile' in request.POST):

            profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=user_profile)

            print("profile pic")

            if profile_pic_form.is_valid():
                print("profile ok")
                profile_pic_form.save()

            messages.success(request, "Profile Picture Updated!")

            return redirect("dashboard")
        

    context = {
        "account_form": account_form,
        "profile_form": profile_form,
        "profile_pic_form": profile_pic_form,
    }


    return render(request, 'account/dashboard.html', context)

def my_profile(request):
    profile = Profile.objects.get(user = request.user)

    reviews = Review.objects.filter(user = request.user).annotate(
        rating_unchecked = 5 - F("rating")
    ).order_by('-time')

    context = {
        "profile": profile,
        "reviews": reviews
    }

    return render(request, 'account/my-profile.html', context)