from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

# Create your views here.

def write_report(request):
    return render(request, "write_report.html")

def create(request):
    new_book = Book()
    new_book.report_name = request.POST['report_name']
    new_book.book_name = request.POST['book_name']
    new_book.category = request.POST['category']
    new_book.content = request.POST['content']