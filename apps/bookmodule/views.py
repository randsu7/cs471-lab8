from .models import Book
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, Student, Address
from django.db.models import Q, Count, Sum, Avg, Max, Min


def index(request):
    return render(request, "bookmodule/index.html")


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))


def list_books(request):
    return render(request, 'bookmodule/list_books.html')


def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')


def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')


def links(request):
    return render(request, 'bookmodule/html5/links.html')


def text_formatting(request):
    return render(request, 'bookmodule/html5/formatting.html')


def listing(request):
    return render(request, 'bookmodule/html5/listing.html')


def tables(request):
    return render(request, 'bookmodule/html5/tables.html')

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower(): contained = True

            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})

    return render(request, 'bookmodule/search.html')

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull = False).filter(title__icontains='and').filter(edition__gte = 2).exclude(price__lte = 100)[:10]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')


def lab8_task1(request):
    mybooks = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8/book_list.html', {'books': mybooks, 'heading': 'Task 1: price less than or equal 80'})


def lab8_task2(request):
    mybooks = Book.objects.filter(Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu')))
    return render(request, 'bookmodule/lab8/book_list.html', {'books': mybooks, 'heading': 'Task 2: edition above 3 and title or author contains qu'})


def lab8_task3(request):
    mybooks = Book.objects.filter(~Q(edition__gt=3) & (~Q(title__icontains='qu') | ~Q(author__icontains='qu')))
    return render(request, 'bookmodule/lab8/book_list.html', {'books': mybooks, 'heading': 'Task 3: edition not above 3 and title or author does not contain qu'})


def lab8_task4(request):
    mybooks = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/lab8/book_list.html', {'books': mybooks, 'heading': 'Task 4: books ordered by title'})


def lab8_task5(request):
    stats = Book.objects.aggregate(
        book_count=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price'),
    )
    return render(request, 'bookmodule/lab8/task5.html', {'stats': stats})


def lab8_task7(request):
    cities = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/lab8/task7.html', {'cities': cities})