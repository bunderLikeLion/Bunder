from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Book

# Create your views here.

# 메인화면
def main(request):
    return render(request, "book_report/book_report.html")

# 독후감 내용 창
def detail_report(request, id):
    book = get_object_or_404(Book, pk = id)
    return render(request, 'book_report/detail_report.html', {'book' : book}) 

# 독후감 작성 창
def write_report(request):
    return render(request, "book_report/write_report.html")

# 독후감 작성 함수
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

# 독후감 수정 창
def edit(request, id):
    edit_book = get_object_or_404(Book, pk = id)
    return render(request, 'book_report/edit_report.html', {'book' : edit_book})

# 독후감 수정 함수
@csrf_exempt
def update(request, id):
    update_book = get_object_or_404(Book, pk = id)
    update_book.report_name = request.POST.get('report_name')
    update_book.book_name = request.POST.get('book_name')
    # update_book.book_author = request.POST.get('book_author')
    update_book.book_category = request.POST.get('book_category')
    update_book.content = request.POST.get('content')
    update_book.save()
    return redirect('book_report:detail', update_book.id)

# 독후감 삭제 함수
def delete(request, id):
    delete_blog = get_object_or_404(Book, pk = id)
    delete_blog.delete()
    return redirect('book_report:main')

# 독후감 검색 함수
def search(request):
    books = Book.objects.all()
    if request.method == "GET":
        search_name = request.GET.get('search_name')
        if search_name:
            books = books.filter(book_name__contains = search_name)
    else:
        search_name = request.POST.get('search_name')
        if search_name:
            books = books.filter(book_name__contains = search_name)
    return render(request, 'book_report/search_report.html', {'books' : books})