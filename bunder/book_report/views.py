from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
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
    populated_report = populated_reports(request)
    all = json.dumps('전체')
    return render(request, "book_report/book_report.html",
                  {'bookReport': book_report, 'page_count': paginator.num_pages, 'page': page,
                   'populate_reports': populated_report, 'category': all })


def category_search(request, category):
    if category == '경제':
        book_report_list = BookReport.objects.filter(book_category='경제/경영').order_by('-created_at')
        page = request.GET.get('page')
        paginator = Paginator(book_report_list, CONTENT_COUNT)
        book_report = paginator.get_page(page)
        populated_report = populated_reports(request)
        category = json.dumps('경제')
    elif category == '정치':
        book_report_list = BookReport.objects.filter(book_category='정치/사회').order_by('-created_at')
        page = request.GET.get('page')
        paginator = Paginator(book_report_list, CONTENT_COUNT)
        book_report = paginator.get_page(page)
        populated_report = populated_reports(request)
        category = json.dumps('정치')
    elif category == '기술':
        book_report_list = BookReport.objects.filter(book_category='기술/IT').order_by('-created_at')
        page = request.GET.get('page')
        paginator = Paginator(book_report_list, CONTENT_COUNT)
        book_report = paginator.get_page(page)
        populated_report = populated_reports(request)
        category = json.dumps('기술')
    else:
        book_report_list = BookReport.objects.filter(book_category=category).order_by('-created_at')
        page = request.GET.get('page')
        paginator = Paginator(book_report_list, CONTENT_COUNT)
        book_report = paginator.get_page(page)
        populated_report = populated_reports(request)
        category = json.dumps(category)
    return render(request, "book_report/book_report.html",
                  {'bookReport': book_report, 'page_count': paginator.num_pages, 'page': page,
                   'populated_report': populated_report, 'category':category})


def write_report(request):
    key = json.dumps(os.environ.get('GOOGLE_BOOK_KEY'));
    return render(request, "book_report/write_report.html", {'bookSecret': key})


def detail_report(request, id):
    book_report = get_object_or_404(BookReport, pk=id)
    book_report_id_json = json.dumps(id)
    commentList = Comment.objects.filter(book_report_id=id)
    user_info = book_report.user
    user = request.user
    if Scrap.objects.filter(user_id__exact=user.id, book_report_id__exact=id).exists():
        boolean = 'True'
    else:
        boolean = 'False'


    return render(request, 'book_report/detail_report.html', {'user_info': user_info, 'book_report': book_report,
                                                              "book_report_id": book_report_id_json,
                                                              "comment": commentList,
                                                              "comment_len": len(commentList), 'boolean': boolean})


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
    new_book.image_upload = request.FILES.get('image_upload')
    new_book.save()
    return redirect('book_report:detail', new_book.id)


def edit(request, id):
    edit_book = get_object_or_404(BookReport, pk=id)
    return render(request, 'book_report/edit_report.html', {'book': edit_book})


@csrf_exempt
def update(request, id):
    update_book = get_object_or_404(BookReport, pk=id)
    update_book.report_name = request.POST.get('report_name')
    update_book.book_name = request.POST.get('book_name')
    update_book.category = request.POST.get('category')
    update_book.content = request.POST.get('content')
    update_book.image_upload = None
    update_book.image_upload = request.FILES.get('image_upload')
    update_book.save()
    return redirect('book_report:detail', update_book.id)


def delete(request, id):
    delete_blog = get_object_or_404(BookReport, pk=id)
    delete_blog.delete()
    return redirect('book_report:main')


# 책 이름을 통한 독후감 검색
def search(request):
    books = BookReport.objects.all()
    if request.method == "GET":
        search_name = request.GET.get('search_name')
        if search_name:
            books = books.filter(book_name__contains=search_name)
    else:
        search_name = request.POST.get('search_name')
        if search_name:
            books = books.filter(book_name__contains=search_name)
    return render(request, 'book_report/search_report.html', {'books': books, 'search_name': search_name})


# 스크랩 하기
@csrf_exempt
def make_scrap(request):
    req = json.loads(request.body)
    book_report_id = req['id']
    if request.method == "POST":
        scrap, created = Scrap.objects.get_or_create(
            book_report=get_object_or_404(BookReport, id=book_report_id),
            user=request.user,
        )

    return JsonResponse({'scrap': model_to_dict(scrap)})


# 스크랩 취소

def del_scrap(request, id):
    noscrap = get_object_or_404(Scrap, pk=id)
    noscrap.delete()
    return HttpResponseRedirect(request.path_info)


# 내 스크랩 확인
class all_scraps(View):
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
    book_report = BookReport.objects.get(id=book_report_id)

    if not request.user.is_authenticated:
        context = {'like_count': book_report.like.count()}
        return HttpResponse(json.dumps(context),
                            content_type='application/json')  # context를 json 형태로 변환, http response 타입 지정(json형태)

    user = request.user
    if book_report.like.filter(id=user.id).exists():
        book_report.like.remove(user)
    else:
        book_report.like.add(user)
    like_count = book_report.like.count()
    book_report.likes = like_count
    book_report.save()
    context = {'like_count': like_count}
    return HttpResponse(json.dumps(context), content_type='application/json')


# 댓글
class CommentRequest(View):

    def post(self, request):
        req = json.loads(request.body)
        book_report_id = req['book_report_id']
        content = req['text']
        if request.user.is_authenticated:
            book_report = get_object_or_404(BookReport, pk=book_report_id)
            comment = Comment()
            comment.user = request.user
            comment.content = content
            comment.book_report = book_report
            comment.save()
            response = {'content': content,
                        'id': comment.id,
                        'nickname': request.user.nickname,
                        'created_at': comment.created_at,
                        'sex': request.user.sex}
            return JsonResponse({'comment': response}
                                , json_dumps_params={'ensure_ascii': False}
                                , status=200)

        else:
            return HttpResponse("로그인 후 이용")

    def delete(self, request):
        req = json.loads(request.body)
        book_report_id = req['bookReportId']
        comments_id = req['commentId']

        comment = get_object_or_404(Comment, pk=comments_id)
        comment.delete()

        return redirect('book_report:detail', id=book_report_id)


# 내 독후감 좋아요 순 3개 확인 함수
def populated_reports(request):
    my_reports = BookReport.objects.all()
    user = request.user
    if user:
        my_reports = my_reports.order_by('-likes')[:3]
    return my_reports
