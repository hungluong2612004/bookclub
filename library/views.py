from django.shortcuts import render, redirect, get_object_or_404
from . models import Category, Book, Author
from shelf.models import ShelfItem
from review.models import Review
from account.models import Profile
from json import dumps 
from django.db.models import Avg, OuterRef, Subquery, Count, Case, When, Q, F
from datetime import timedelta, datetime
from django.conf import settings

# from django.contrib.postgres.aggregates import ArrayAgg, StringAgg

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

import requests, wikipediaapi
import json


from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)


# Create your views here.

def library(request):
   
    primary_category = Book.objects.filter(id = OuterRef("id")).values("category")[:1]
    category_name = Category.objects.filter(id = OuterRef("primary_category")).values("name")
    books = Book.objects.all().annotate(
        primary_category = Subquery(primary_category),
        category_name = Subquery(category_name))
    
    trending_books = Book.objects.all().annotate(
        primary_category = Subquery(primary_category), 
        category_name = Subquery(category_name),
        review_count = Count("reviews", filter = Q(reviews__time__gt = datetime.today()-timedelta(days=30)))
        ).order_by('-review_count')[0:5]
    

    context = {
        "books": books,
        "trending_books": trending_books,
    }
    return render(request, 'library/library.html', context)

def categories(request): 
    all_categories = Category.objects.all()

    context = {'all_categories': all_categories}

    return(context)

def list_category(request, category_slug):

    single_category = Category.objects.get(slug = category_slug)

    books = Book.objects.filter(category = single_category)
    

    context = {'books': books, 'single_category': single_category}

    return render(request, 'library/category.html', context)

def book_info(request, book_slug):
    book = get_object_or_404(Book, slug = book_slug)
    try:
        shelf_item = ShelfItem.objects.get(book = book, user = request.user)
        shelf = shelf_item.shelf
    except:
        shelf = "not added"

    try:
        user_review = Review.objects.get(book = book, user = request.user)
        rating = user_review.rating
    except:
        rating = "unrated"
    
   
    
    numOfReviews = Review.objects.filter(book = book).count()
    reviews = Review.objects.filter(book = book)

    sum = 0

    for review in reviews:
        sum += review.rating
   
    avgRating = 0
    if(numOfReviews > 0):
        avgRating = sum/numOfReviews

    
    data = {
        "rating": rating,
        "numOfReviews": numOfReviews,
        "avgRating": avgRating,
    }
    dataJSON = dumps(data)

    
    context = {
        "book": book, 
        "shelf": shelf,
        "rating": rating,
        "numOfReviews": numOfReviews,
        "avgRating": avgRating,
        "allreviews": reviews,
        "data": dataJSON
    }


    return render(request, 'library/book-info.html', context)


def search(request):

    keyword = str(request.GET.get("keyword"))

    result = Book.objects.filter(
        Q(category__name__contains = keyword) | Q(author__name__contains = keyword) | Q(title__contains = keyword)
    ).distinct()
    
    context = {
        "keyword": keyword, 
        "result": result
    }

    print("keyword is", keyword)
    return render(request, 'library/search.html', context)      

def author_info(request, author_slug):
    author = get_object_or_404(Author, slug = author_slug)

    wiki_wiki = wikipediaapi.Wikipedia('bookclub (hungnc888@gmail.com)' , 'en')


    author_wiki_slug = "_".join(map(lambda x: x.capitalize(), author.slug.split('-')))
    print(author_wiki_slug)
    author_summary = " ".join(wiki_wiki.page(author_wiki_slug).summary.split('.')[0:2]) + "."

    books = Book.objects.filter(author = author).annotate(rating = Avg("reviews__rating"), review_count = Count("reviews"))

    avg_rating = Review.objects.filter(book__author = author).aggregate(Avg("rating"))


    context = {
        "author": author,
        "books": books,
        "avg_rating": avg_rating,
        "author_summary": author_summary
    }

    return render(request, 'library/author-info.html', context)

@login_required(login_url = 'login')
def for_you(request):

    primary_category = Book.objects.filter(id = OuterRef("id")).values("category")[:1]
    category_name = Category.objects.filter(id = OuterRef("primary_category")).values("name")

    #review_count is to count the number reviews of each book that are created in the past 30 days

    all_books = Book.objects.all().annotate(
        primary_category = Subquery(primary_category), 
        category_name = Subquery(category_name),
        review_count = Count("reviews", filter = Q(reviews__time__gt = datetime.today()-timedelta(days=30)))
        ).order_by('-review_count')
    
    trending_books = all_books[0:8]


    # for book in all_books:
    #     print(book.title, "review", book.review_count)


    added = ShelfItem.objects.filter(book = OuterRef("id"), user = request.user).values("shelf")
    notadded_books = Book.objects.annotate(
        added = Subquery(added)
    ).filter(added = None)

    author = Author.objects.filter(book = OuterRef("book")).values("name")
    authors_on_shelf = ShelfItem.objects.filter(user = request.user).annotate(author = Subquery(author))\
    .values('author').order_by('author').annotate(book_count = Count('author')).order_by('-book_count')

    liked_author = []
    for author in authors_on_shelf:
        author_info = Author.objects.get(name = author["author"])
        liked_author.append({
            "info": author_info, 
            "book_count": author["book_count"]})
        
    print("AUTHOR", liked_author)
    
    authors2 = ShelfItem.objects.filter(user = request.user).values('book__author__name').order_by('book__author__name').annotate(book_count = Count('book__author__name')).order_by('-book_count')
    # authors2 and authors_on_shelf do the same thing, but authors_on_shelf is easier to for user to read


    recommended_list = []
    for author in authors_on_shelf:
        should_read = Book.objects.annotate(
            added = Subquery(added)
        ).filter(added = None, author__name = author["author"]).annotate(primary_category = Subquery(primary_category), category_name = Subquery(category_name))
        for book in should_read:
            recommended_list.append(book)

    liked_categories = Profile.objects.get(user = request.user).liked_categories.all()

    for book in all_books:
        liked = False
        for category in book.category.all():
            if category in liked_categories:
                liked = True
                break
        if liked and (book in notadded_books) and (book not in recommended_list):
            recommended_list.append(book)

    print("recommended", recommended_list)



   
    context = {
        "notadded_books": notadded_books,
        "authors_on_shelf": authors_on_shelf,
        "recommended_list": recommended_list,
        "trending_books": trending_books,
        "liked_author": liked_author,
    }
    return render(request, 'library/for_you.html', context)

@login_required(login_url = 'login')
def discover(request):

    author = Author.objects.filter(book = OuterRef("book")).values("name")
    authors_on_shelf = ShelfItem.objects.filter(user = request.user).annotate(author = Subquery(author))\
    .values('author').order_by('author').annotate(book_count = Count('author')).order_by('-book_count')[:2]

    import functools
    import operator

    genres = ShelfItem.objects.filter(user = request.user).values('book__category__name').order_by('book__category__name').annotate(category_count = Count('book__category__name')).order_by('-category_count')[:2]
    fav_genres = []
    for genre in genres:
        fav_genres.append(genre["book__category__name"])
        # print (genre["book__category__name"], genre["category_count"])


    fav_authors = []
    for author in authors_on_shelf:
        fav_authors.append(author['author'])

    print("fav is", fav_authors)
    print("fav is", fav_genres)

    author_prompt = ", ".join(fav_authors)
    genres_prompt = ", ".join(fav_genres)

    reason = "and a short reason of under 10 words i might like it."

    requirement = ". Give answer in form of json with primary field books, each element with fields title, author, genre"

    requirement = ". Give answer in form of book name, author and genre"

    prompt = "My favorite authors are " + author_prompt + ". My favorite genres are " + genres_prompt + ". Give me 4 book recommendations from 4 other authors" + requirement

    print("prompt is", prompt)

    new_prompt = "%20".join(prompt.split(" "))
    from openai import OpenAI
    # client = OpenAI()

    # completion = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "system", "content": "You give book recommendations"},
    #     {"role": "user", "content": prompt}
    # ]
    # )

    # print(completion.choices[0].message)    

    data = {
        "apiKey": settings.OPENAI_API_KEY, "prompt": new_prompt
    }

    print("key is", settings.OPENAI_API_KEY)

    dataJSON = dumps(data)

    context = {
        "data": dataJSON
    }



    return render(request, 'library/discover.html', context)