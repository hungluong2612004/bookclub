from django.urls import path

from . import views

urlpatterns = [
    path('add-rating', views.add_rating, name = 'add-rating'),
    path('add-comment/<slug:book_slug>', views.add_comment, name = 'add-comment'),
    path('save-review', views.update_review, name = 'update-review'),
]