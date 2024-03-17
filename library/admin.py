from django.contrib import admin

# Register your models here.

from .models import Category, Book, Author

@admin.register(Category)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Author)

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}