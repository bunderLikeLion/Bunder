from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Book

# Create your views here.

def write_report(request):
    return render(request, "book_report/write_report.html")

def detail_report(request, id):
    book = get_object_or_404(Book, pk = id)
    return render(request, 'book_report/detail_report.html', {'book' : book}) 

@csrf_exempt
def create(request):
    new_book = Book()
    new_book.report_name = request.POST['report_name']
    new_book.book_name = request.POST['book_name']
    # new_book.book_author = request.POST.get('book_author')
    new_book.book_category = request.POST['book_category']
    new_book.content = request.POST['content']
    new_book.save()
    return redirect('book_report:detail', new_book.id)