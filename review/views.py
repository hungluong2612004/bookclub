from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse

from .models import Review

from library.models import Book
from shelf.models import ShelfItem, ShelfOption

from json import dumps 

from django.contrib.auth.decorators import login_required

@login_required(login_url = 'login')
def add_rating(request):
    if request.POST.get("action") == 'POST':

        print("adding rating")

        book_id = request.POST.get("book_id")
        rating = int(request.POST.get("rating"))

        book = get_object_or_404(Book, id = book_id)
    
        Review.objects.create(
            user = request.user,
            book = book,
            rating = rating
        )

        try:
            book_on_shelf = ShelfItem.objects.get(book = book, user = request.user)
            book_on_shelf.shelf = ShelfOption.objects.get(shelf_option = "read")
            book_on_shelf.save()

        except:
            ShelfItem.objects.create(
                user = request.user,
                book = book,
                shelf = ShelfOption.objects.get(shelf_option = "read")
            )
        
    response = JsonResponse({
            'message': 'added to review'
        })

    return response

@login_required(login_url = 'login')
def add_comment(request, book_slug):

    book = get_object_or_404(Book, slug = book_slug)

    try:
        review = Review.objects.get(book = book, user = request.user)
        rating = review.rating
        comment = review.comment
        # time = str(review.time)
        # print("time", time[0:10])

    except:
        rating = "unrated"
        comment = "None"     

    try:
        book_on_shelf = ShelfItem.objects.get(book = book, user = request.user)
        book_on_shelf.shelf = ShelfOption.objects.get(shelf_option = "read")
        book_on_shelf.save()
            
    except:
        ShelfItem.objects.create(
            user = request.user,
            book = book,
            shelf = ShelfOption.objects.get(shelf_option = "read")
        )
           
    
    print("review is", rating, comment)

    data = {
        "book_id": book.id,
        "rating": rating,
        "comment": comment
    }

    dataJSON = dumps(data)

    context = {
        "book": book,
        "rating": rating,
        "comment": comment,
        "data": dataJSON
    }

    return render(request, 'review/book-review.html', context)

@login_required(login_url = 'login')
def update_review(request):

    if request.POST.get("action") == 'POST':
        book_id = request.POST.get("book_id")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment").strip()
        user = request.user

        print(book_id, rating, comment, user)

        book = get_object_or_404(Book, id = book_id)

        try:
            review = Review.objects.get(user = user, book = book)

            print("time", review.time)

            review.rating = rating
            if(comment != ""):
                review.comment = comment
            review.save()

            return redirect("library")


        except:
            if(comment == ""):
                Review.objects.create(
                    user = request.user,
                    book = book,
                    rating = rating
                )
            else:
                Review.objects.create(
                    user = request.user,
                    book = book,
                    rating = rating,
                    comment = comment
                )
            
            return redirect("library")


    response = JsonResponse({
            'message': 'review updated'
        })

    print("redirecting ")
    return response
    # return redirect("book-info", book_slug = book.slug)