from django.urls import path

from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name = 'sign-up'),
    path('login', views.my_login, name = 'login'),
    path('logout', views.user_logout, name = 'logout'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('my-profile', views.my_profile, name = 'my-profile')
]