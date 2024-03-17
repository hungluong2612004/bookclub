from django.db import models

from django.contrib.auth.models import User

from library.models import Book

from django.urls import reverse


# Create your models here.

class ShelfOption(models.Model):
    shelf_option = models.CharField(max_length = 50, db_index=True)
    slug = models.SlugField(max_length=250, unique = True)

    class Meta:
        verbose_name_plural = "Shelf Option"

    def __str__(self):
        return self.shelf_option
    
    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])
    
class ShelfItem(models.Model):
    shelf = models.ForeignKey(ShelfOption, related_name = "shelf_item", on_delete= models.CASCADE)
    # shelf_option = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE) 

    class Meta:
        verbose_name_plural = "Shelf Item"

    def __str__(self): 
        return 'Shelf Item - ' + str(self.id)
