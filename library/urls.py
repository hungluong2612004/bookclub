from django.urls import path
from . import views

urlpatterns = [
    path("", views.library, name = "library"),
    path("category/<slug:category_slug>", views.list_category, name = "list-category"),
    path("book-info/<slug:book_slug>", views.book_info, name = "book-info"),
    path("search", views.search, name = "search"),
    path("for-you", views.for_you, name = "for-you"),
    path("discover", views.discover, name = "discover"),
    path("author-info/<slug:author_slug>", views.author_info, name = "list-author")
]
