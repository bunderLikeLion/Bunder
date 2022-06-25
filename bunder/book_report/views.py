from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import BookReport, Scrap, Comment
from django.views import View
import json
import os
# Create your views here.

CONTENT_COUNT = 9

def main(request):
    book_report_list = BookReport.objects.filter().order_by('-created_at')
    page = request.GET.get('page')
    paginator = Paginator(book_report_list, CONTENT_COUNT)
    book_report = paginator.get_page(page)

    return render(request, "book_report/book_report.html", {'bookReport': book_report, 'page_count': paginator.num_pages, 'page': page})

def category_search(request, category):
    book_report_list = BookReport.objects.filter(book_category=category).order_by('-created_at')
    page = request.GET.get('page')
    paginator = Paginator(book_report_list, CONTENT_COUNT)
    book_report = paginator.get_page(page)

    return render(request, "book_report/book_report.html", {'bookReport': book_report, 'page_count': paginator.num_pages, 'page': page})

def write_report(request):
    key = json.dumps(os.environ.get('GOOGLE_BOOK_KEY'));
    return render(request, "book_report/write_report.html", {'bookSecret': key})

def detail_report(request, id):
    book_report = get_object_or_404(BookReport, pk = id)
    book_report_id_json = json.dumps(id)
    commentList = Comment.objects.filter(book_report_id=id)

    return render(request, 'book_report/detail_report.html', {'book_report' : book_report, "book_report_id": book_report_id_json, "comment": commentList})

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


# 독후감 좋아요 기능 및 좋아요 취소 (비동기식 ajax)
def likes(request):
    book_report_id = request.GET['book_report_id']
    book_report = BookReport.objects.get(id = book_report_id)

    if not request.user.is_authenticated:
        context = {'like_count' : book_report.like.count()}
        return HttpResponse(json.dumps(context), content_type = 'application/json') # context를 json 형태로 변환, http response 타입 지정(json형태)

    user = request.user
    if book_report.like.filter(id = user.id).exists():
        book_report.like.remove(user)
    else:
        book_report.like.add(user)
    like_count = book_report.like.count()
    book_report.likes = like_count
    book_report.save()
    context = {'like_count' : like_count}
    return HttpResponse(json.dumps(context), content_type = 'application/json')

#댓글 작성
class CreateComment(View):

    def post(self, request):
        req = json.loads(request.body)
        book_report_id = req['book_report_id']
        content = req['text']
        if request.user.is_authenticated:
            book_report = get_object_or_404(BookReport, pk = book_report_id)
            comment = Comment()
            comment.user = request.user
            comment.content = content
            comment.book_report = book_report
            comment.save()
            response = {'content' : content,
                        'nickname': request.user.nickname,
                        'created_at': comment.created_at}
            return JsonResponse({'comment': response }
                                , json_dumps_params={'ensure_ascii': False}
                                , status=200)

        else:
            return HttpResponse("로그인 후 이용")



# 댓글 수정
# 댓글 삭제
# 댓글 좋아요기능
# 댓글 좋아요취소