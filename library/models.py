from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique = True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])
    

class Author(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique = True)
    description = models.TextField(max_length = 4000, null = True, blank = True)
    image = models.ImageField(null = True, blank = True, default = 'images/default.jpeg', upload_to='images/') #allow author to not have a profile pic (profile_pic = none), otherwise there's gonna be bug
    
    class Meta:
        verbose_name_plural = "authors"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list-author', args=[self.slug])

    
   
class Book(models.Model):

    # primary_category = models.ForeignKey(Category, null = True, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    title = models.CharField(max_length=250)
    # author = models.CharField(max_length=250)
    author = models.ForeignKey(Author, null = True, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    slug = models.SlugField(max_length=250, unique = True)
    description = models.TextField(max_length=10000, null = True, blank = True)
    image = models.ImageField(upload_to= "images/")

    class Meta:
        verbose_name_plural = "books"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-info', args=[self.slug])
