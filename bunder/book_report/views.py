from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

# Create your views here.

def write_report(request):
    return render(request, "write_report.html")

def create(request):
    new_book = Book()
    new_book.book_title = request.POST['title']