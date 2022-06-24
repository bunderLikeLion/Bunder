from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import BookReport, Scrap, Comment
from django.views import View
import json
import os
# Create your views here.

def main(request):
    return render(request, "book_report/book_report.html")

def write_report(request):
    key = json.dumps(os.environ.get('GOOGLE_BOOK_KEY'));
    return render(request, "book_report/write_report.html", {'bookSecret': key})

def detail_report(request, id):
    book_report = get_object_or_404(BookReport, pk = id)
    book_report_id_json = json.dumps(id)
    return render(request, 'book_report/detail_report.html', {'book_report' : book_report, "book_report_id": book_report_id_json})

@csrf_exempt
def create(request):
    new_book = BookReport()
    new_book.user = request.user
    new_book.report_name = request.POST.get('report_name')
    new_book.book_name = request.POST.get('book_name')
    new_book.book_author = request.POST.get('book_author')
    new_book.book_img = request.POST.get('book_img')
    new_book.book_category = request.POST.get('book_category')
    new_book.content = request.POST.get('content')
    new_book.save()
    return redirect('book_report:detail', new_book.id)

def edit(request, id):
    edit_book = get_object_or_404(BookReport, pk = id)
    return render(request, 'book_report/edit_report.html', {'book' : edit_book})

@csrf_exempt
def update(request, id):
    update_book = get_object_or_404(BookReport, pk = id)
    update_book.report_name = request.POST.get('report_name')
    update_book.book_name = request.POST.get('book_name')
    update_book.category = request.POST.get('category')
    update_book.content = request.POST.get('content')
    update_book.save()
    return redirect('book_report:detail', update_book.id)

def delete(request, id):
    delete_blog = get_object_or_404(BookReport, pk = id)
    delete_blog.delete()
    return redirect('book_report:main')

# 책 이름을 통한 독후감 검색
def search(request):
    books = BookReport.objects.all()
    if request.method == "GET":
        search_name = request.GET.get('search_name')
        if search_name:
            books = books.filter(book_name__contains = search_name)
    else:
        search_name = request.POST.get('search_name')
        if search_name:
            books = books.filter(book_name__contains = search_name)
    return render(request, 'book_report/search_report.html', {'books' : books})

#스크랩 하기
@csrf_exempt
def make_scrap(request):
    req = json.loads(request.body)
    book_report_id = req['id']
    print("독후감 아이디 " + str(book_report_id))
    if request.method == "POST":
        scrap, created = Scrap.objects.get_or_create(
            book_report=get_object_or_404(BookReport, id=book_report_id),
            user=request.user,
        )

    return JsonResponse({'scrap': model_to_dict(scrap)})

# 내 스크랩 확인
class all_my_scraps(View):
    def get(self, request):
        scraps = Scrap.objects.filter(user_id=request.user.id)
        report = []
        
        for scrap in scraps:
            book_report = BookReport.objects.get(pk=scrap.book_report_id)
            report.append(book_report)
            print(book_report.report_name)

        return render(request, 'user/all_my_scraps.html',
                      {'user': request.user, 'book_report': report})

#댓글 작성
@csrf_exempt
def comment_create(request, book_report_id):
    print('addd')
    if request.user.is_authenticated:
        book_report = get_object_or_404(BookReport, pk = book_report_id)
        comment = Comment()
        if request.method == "POST":
            comment.user = request.user
            comment.content = request.POST.get('comment_content')
            comment.book_report = book_report
            comment.save()
            return render(request, 'book_report/detail_report.html', {'comment' : comment})
        return redirect('book_report:detail', book_report_id)  
    else:  
        return HttpResponse("로그인 후 이용")
        


# 댓글 수정
# 댓글 삭제
# 댓글 좋아요기능
# 댓글 좋아요취소