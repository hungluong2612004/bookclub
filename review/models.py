from django.db import models

from django.contrib.auth.models import User

from library.models import Book

from datetime import datetime


# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    comment = models.TextField(max_length=10000, blank=True, null=True)
    time = models.DateTimeField("updated_time", auto_now=True)


    class Meta:
        verbose_name_plural = "Review"

    def __str__(self): 
        return 'Review - ' + str(self.id)

