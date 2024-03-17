from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse

from . models import ShelfItem, ShelfOption

from review.models import Review

from library.models import Book

from json import dumps 

from django.db.models import Avg, OuterRef, Subquery, Count, Case, When, Q

from django.contrib.auth.decorators import login_required


@login_required(login_url = 'login')
def my_books(request, shelf_option):

    current_shelf = "all"
    if(shelf_option != "all"):
        current_shelf = ShelfOption.objects.get(slug = shelf_option).shelf_option
    
    
    reviews = Review.objects.filter(book = OuterRef("id"), user =request.user).values('rating')
    shelf= ShelfItem.objects.filter(book = OuterRef("id"), user = request.user).values('shelf')
    #the field in the OuterRef("") of the Subquery refers to the field of the Model of the parent query
    shelf_name = ShelfOption.objects.filter(id = OuterRef("shelf")).values('shelf_option')
    my_books =  Book.objects.annotate(
        rating_by_this_user = Subquery(reviews), 
        shelf = Subquery(shelf), 
        shelf_name = Subquery(shelf_name),
        avg_rating = Avg('reviews__rating')
    )

    print(ShelfItem.objects.all().query)
    print(Book.objects.all().query)

    num_of_books = len(ShelfItem.objects.filter(user = request.user))

    all_shelves = ShelfOption.objects.annotate(number_of_items = Count(
        "shelf_item",
        filter = Q(shelf_item__user = request.user)
    ))


    for book in my_books:
        print(book.title, "review is", book.rating_by_this_user, "shelf is", book.shelf_name, "avg rating is", book.avg_rating)
    
    # for shelf in all_shelves:
    #     print(shelf.shelf_option, "is", shelf.id, "number", shelf.number_of_items)
    
    data = {
        "current_shelf": current_shelf,
    }
    dataJSON = dumps(data)
    #dataJSON is used to pass data to js in html file

    context = {
        "my_books": my_books,
        "num_of_books": num_of_books,
        "all_shelves": all_shelves,
        "current_shelf": current_shelf,
        "data": dataJSON
    }
    
    return render(request, 'shelf/my-books.html', context)

@login_required(login_url = 'login')
def update_shelf(request):
    if request.POST.get('action') == 'POST':
        print("FJLDKFJLDKJFLK")
        book_id = str(request.POST.get('book_id'))
        shelf_option = str(request.POST.get('shelf_option'))

        shelf = get_object_or_404(ShelfOption, shelf_option = shelf_option)
        book = get_object_or_404(Book, id = book_id)

        try: 

            book_on_shelf = ShelfItem.objects.get(book = book, user = request.user)
            book_on_shelf.shelf = shelf
            book_on_shelf.save()
            print("the book on shelf is", book_on_shelf.book.title)
    
        except:

            print("my book is", book.title)

            ShelfItem.objects.create(
                shelf = shelf,
                user = request.user,
                book = book
            )

        response = JsonResponse({
            'message': 'added to shelf'
        })

        return response

@login_required(login_url = 'login')
def remove(request):
    if request.POST.get("action") == 'POST':
        book_id = str(request.POST.get('book_id'))
        book = get_object_or_404(Book, id = book_id)
        book_on_shelf = get_object_or_404(ShelfItem, book = book, user = request.user)
        book_on_shelf.delete()

        response = JsonResponse({
            'message': 'added to shelf'
        })

        return response

