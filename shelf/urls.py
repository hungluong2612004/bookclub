from django.urls import path

from . import views

urlpatterns = [
    path('book-list/<slug:shelf_option>', views.my_books, name = 'my-books'),
    path('remove', views.remove, name = 'remove'),
    path('update-shelf', views.update_shelf, name = 'update-shelf')
]