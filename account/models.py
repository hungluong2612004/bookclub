from django.db import models

from library.models import Category

from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    profile_pic = models.ImageField(null = True, blank = True, default = 'images/default.jpeg', upload_to='images/') #allow user to not have a profile pic (profile_pic = none), otherwise there's gonna be bug

    city = models.TextField(max_length=100, null=True, blank=True)
    country = CountryField(null = True, blank=True)
    about_me = models.TextField(max_length=10000, null = True, blank= True)

    liked_categories = models.ManyToManyField(Category)
    # liked_categories = MultiSelectField(choices=Category)

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return "Profile - " + self.user.username