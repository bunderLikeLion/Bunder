from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.views import View
import json
import os
from .models import BookClub, BookClubVote, VoteDetail, BookClubMember, Book


def main(request):
    book_club = getBookClub()
    my_club = getMyBookClub(request.user)
    return render(request, "book_club/book_club.html", {'book_club': book_club, 'my_club': my_club})


def book_club_list(request):
    if request.method == "GET":
        category = request.GET.get("category")
        page = request.GET.get('page')
        if category == "인기":
            club_list = BookClub.objects.all().order_by('-created_at')
        else:
            club_list = BookClub.objects.filter(category=category).order_by('-created_at')
        paginator = Paginator(club_list, 10)
        club_list = paginator.get_page(page)
        return render(request, "book_club/category_clubs.html",
                      {'club_list': club_list,
                       'category': category,
                       'total': paginator.count})




@csrf_exempt
def new(request):
    if request.method == "GET":
        return render(request, 'book_club/add_club.html')
    elif request.method == "POST":

        book_club = BookClub()
        book_club.owner = request.user
        book_club.club_name = request.POST["clubname"]
        book_club.member_total = request.POST["number_of_member"]
        book_club.image = request.POST["club_img"]
        book_club.category = request.POST["book_category"]
        book_club.description = request.POST["content"]
        book_club.save()

        member, created = BookClubMember.objects.get_or_create(
            club=get_object_or_404(BookClub, id=book_club.id),
            user=request.user,
            type=BookClubMember.type_enum[2][0]  # 소모임장
        )

        if request.POST.get('link', True):
            book_club.link = request.POST["link"]

        return redirect('/bookclub/' + str(book_club.id))


def book_club_detail(request, bookclub_id):
    book_club = get_object_or_404(BookClub, id=bookclub_id)
    bookclub_id_json = json.dumps(book_club.id)

    try:
        book = Book.objects.filter(club_id=bookclub_id, active=True).first()
        vote = BookClubVote.objects.get(club=book_club)
        vote_id_json = json.dumps(vote.id)
        return render(request, 'book_club/club_detail.html',
                      {'book_club': book_club,
                       'bookclub_id': bookclub_id_json,
                       'vote': vote,
                       'vote_id': vote_id_json,
                       'book_info': book})
    except BookClubVote.DoesNotExist:
        return render(request, 'book_club/club_detail.html',
                      {'book_club': book_club, 'bookclub_id': bookclub_id_json,
                       'book_info': book})


class club_admit(View):
    def get(self, request):
        clubId = request.GET.get('clubId', None)
        members = BookClubMember.objects.prefetch_related('club').filter(club_id=clubId, type="CANDIDATE")
        book_club = get_object_or_404(BookClub, id=clubId)
        return render(request, 'book_club/club_admit.html',
                      {'members': members, 'book_club': book_club})

    def patch(self, request):
        req = json.loads(request.body)
        memberId = req['memberId']
        type = req['type']
        member = BookClubMember.objects.get(pk=memberId)
        club = member.club

        if member.type == "MEMBER":
            return JsonResponse({"message": "이미 멤버로 추가된 유저입니다.",
                                 }, json_dumps_params={'ensure_ascii': False}, status=400)

        member.type = type
        member.save()

        total, curr_cnt = member.get_club_cnt()

        if curr_cnt < total and type == "MEMBER":
            club.add_member_cnt()
            club.save()

            club_response = {'clubName': club.club_name,
                             'memberCnt': club.member_cnt,
                             'maxCnt': club.member_total
                             }

            member_response = {'nickname': member.user.nickname,
                               'type': member.type}

            return JsonResponse({'member': member_response,
                                 'club': club_response})
        elif type == "REJECT":
            return JsonResponse({'message': "멤버를 거절하였습니다.",
                                 'member': model_to_dict(member)
                                 }, json_dumps_params={'ensure_ascii': False}, status=200)
        else:
            return JsonResponse({'message': "인원수 초과 입니다.",
                                 }, json_dumps_params={'ensure_ascii': False}, status=400)


@csrf_exempt
def request_member(request):
    if request.method == "POST":
        req = json.loads(request.body)
        bookclub_id = req['id']
        member, created = BookClubMember.objects.get_or_create(
            club=get_object_or_404(BookClub, id=bookclub_id),
            user=request.user,
        )

        return JsonResponse({'member': model_to_dict(member)})


class AddVote(View):
    def get(self, request):
        clubId = request.GET.get('clubId', None)
        club = BookClub.objects.get(id=clubId)
        if club.owner_id != request.user.id:
            # TODO: 권한 없음 에러페이지 헨들링
            return redirect("/")
        return render(request, 'book_club/add_vote.html')

    def post(self, request):
        clubId = request.GET.get('clubId', None)
        club = BookClub.objects.get(id=clubId)

        if club.owner_id != request.user.id:
            # TODO: 권한 없음 에러페이지 헨들링
            return redirect("/")

        vote_list = request.POST.getlist('input[]')
        vote = BookClubVote()
        vote.club = club
        vote.topic = request.POST['topic']
        vote.start_date = request.POST['startvote']
        vote.end_date = request.POST['endvote']

        vote.save()
        voteList = []
        for each_vote in vote_list:
            vote_detail = VoteDetail()
            vote_detail.description = each_vote
            vote_detail.vote = vote
            vote_detail.save()
            voteList.append(vote_detail)

        return redirect('/bookclub/' +
                        str(clubId))

    def delete(self, request):
        clubId = request.GET.get('clubId', None)

        try:
            vote = BookClubVote.objects.get(club_id=clubId)
            vote.delete()
            return JsonResponse({"description": "투표가 삭제 되었습니다.",
                                 }, json_dumps_params={'ensure_ascii': False}, status=200)
        except BookClubVote.DoesNotExist:
            return JsonResponse({"description": "현재 진행중인 투표가 없습니다."}
                                , json_dumps_params={'ensure_ascii': False},
                                status=404)


class Vote(View):

    def get(self, request):
        clubId = request.GET.get('clubId', None)
        voteId = request.GET.get('voteId', None)
        club = BookClub.objects.get(id=clubId)
        vote = BookClubVote.objects.get(id=voteId)
        voteList = VoteDetail.objects.filter(vote_id=voteId)

        if club.owner_id != request.user.id:
            # TODO: 권한 없음 에러페이지 헨들링
            return redirect("/")

        return render(request, 'book_club/vote.html', {'vote': vote, 'voteList': voteList})

    def post(self, request):
        vote_detail_id = request.POST['vote']
        vote_detail = VoteDetail.objects.get(id=vote_detail_id)
        vote_detail.vote_cnt += 1
        vote_detail.save()

        vote = BookClubVote.objects.get(id=vote_detail.vote_id)

        return redirect("/bookclub/" + str(vote.club.id))


class ClubBook(View):
    def get(self, request):
        key = json.dumps(os.environ.get('GOOGLE_BOOK_KEY'))
        clubId = request.GET.get('clubId', None)
        json_clubId = json.dumps(clubId)
        return render(request, 'user/add_book.html', {'bookSecret': key, 'clubId': json_clubId})

    @csrf_exempt
    def post(self, request):
        book = Book()
        clubId = request.GET.get('clubId')
        try:
            find_book = Book.objects.get(club_id=clubId, active=True)
            find_book.delete()
        except Book.DoesNotExist:
            pass
        book.club = BookClub.objects.get(pk=clubId)
        book.book_name = request.POST.get('book_name')
        book.book_author = request.POST.get('book_author')
        book.book_img = request.POST.get('book_img')
        book.category = request.POST.get('book_category')
        book.active = True
        book.save()

        return redirect('book_club:book_club_detail', clubId)


def getBookClub():
    literature = BookClub.objects.filter(category="문학").order_by('-created_at')[0:3]
    humanities = BookClub.objects.filter(category="인문").order_by('-created_at')[0:3]
    economy = BookClub.objects.filter(category="경제/경영").order_by('-created_at')[0:3]
    self_development = BookClub.objects.filter(category="자기계발").order_by('-created_at')[0:3]
    political_society = BookClub.objects.filter(category="정치/사회").order_by('-created_at')[0:3]
    art = BookClub.objects.filter(category="예술").order_by('-created_at')[0:3]
    science = BookClub.objects.filter(category="과학").order_by('-created_at')[0:3]
    it = BookClub.objects.filter(category="기술/IT").order_by('-created_at')[0:3]
    amity = BookClub.objects.filter(category="자율").order_by('-created_at')[0:3]

    book_club = {
        'literature': literature,
        'humanities': humanities,
        'economy': economy,
        'self_development': self_development,
        'political_society': political_society,
        'art': art,
        'science': science,
        'it': it,
        'amity': amity
    }

    return book_club


def getMyBookClub(user):
    query = Q()
    query.add(Q(user_id=user.id), query.AND)
    query.add(Q(type="OWNER") | Q(type="MEMBER"), query.AND)

    book_club_member = BookClubMember.objects.prefetch_related('club').filter(query)
    club_list = [memberclub.club for memberclub in book_club_member]

    return club_list
