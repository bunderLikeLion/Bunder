import datetime
from math import ceil

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.views import View
from user.models import User
import json
import os
from django.db import connection
from .models import BookClub, BookClubVote, VoteDetail, BookClubMember, Book, VoteCheck

import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember


def getInvitedClub(user):
    club_member = BookClubMember.objects.prefetch_related('club').filter(user=user, type="INVITE")
    club = [member.club for member in club_member]
    return club


def main(request):
    book_club = getBookClub()

    query = Q()
    query.add(Q(user=request.user), query.AND)
    query.add(Q(type="OWNER") | Q(type="MEMBER"), query.AND)

    result = get_my_book_club(request)
    invited_club = getInvitedClub(request.user)
    total_json = json.dumps(result['total_cnt'])
    return render(request, "book_club/book_club.html", {'book_club': book_club, 'my_club': result['club_list'],
                                                        'total_cnt': result['total_cnt'],
                                                        'invited_club': invited_club,
                                                        'total_json': total_json})


def get_my_book_club(request):
    if request.method == 'GET':
        user = request.user

        page = int(request.GET.get("page", 1) or 1)

        query = Q()
        query.add(Q(user=user), query.AND)
        query.add(Q(type="OWNER") | Q(type="MEMBER"), query.AND)

        book_club_member = BookClubMember.objects.prefetch_related('club').filter(query).order_by('-id')

        paginator = Paginator(book_club_member, 3)
        club_list_page = paginator.get_page(page)

        club_list = [model_to_dict(member.club) for member in club_list_page]
        result = {'club_list': club_list, 'total_cnt': paginator.num_pages}
        return result


def get_my_book_club_json(request):
    result = get_my_book_club(request)
    return JsonResponse({'club_list': result['club_list'], 'total_cnt': result['total_cnt']},
                        json_dumps_params={'ensure_ascii': False}, status=200)


def book_club_list(request):
    if request.method == "GET":
        category = request.GET.get("category")
        page = request.GET.get('page')
        if category == "인기":
            club_list = BookClub.objects.all().order_by('-score')
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

    book_club.view += 1
    book_club.score += 1
    book_club.save()

    bookclub_id_json = json.dumps(book_club.id)
    user_id_json = json.dumps(request.user.id)
    is_owner = True if request.user == book_club.owner else False

    query = Q()
    query.add(Q(club=book_club), query.AND)
    query.add(Q(type="OWNER") | Q(type="MEMBER"), query.AND)

    member_list = BookClubMember.objects.prefetch_related("user").filter(query)
    user_list = [member.user for member in member_list]

    is_member = True if request.user in user_list else False


    try:
        book = Book.objects.filter(club_id=bookclub_id, active=True).first()
        book_id_json = None

        if book:
            book_id_json = json.dumps(book.id)
        book_list = get_book(bookclub_id)
        is_full = True if len(book_list) >= 5 else False
        is_full_json = json.dumps(is_full)

        end_vote, vote, vote_id_json, end_vote_list, onset_list = None, None, None, None, None
        check = False

        if BookClubVote.objects.filter(club=book_club, active=True).exists():
            vote = BookClubVote.objects.get(club=book_club, active=True)
            end_date = vote.end_date
            today = datetime.datetime.now()
            if today > end_date:
                vote.active = False
                vote.save()
                vote = None
            else:
                vote_id_json = json.dumps(vote.id)

            try:
                vote_check = VoteCheck.objects.get(vote=vote, user=request.user)
                check = vote_check.checked
            except:
                pass


        if BookClubVote.objects.filter(club=book_club, active=False).exists():
            end_vote = BookClubVote.objects.filter(club=book_club, active=False).order_by('-created_at')[0]
            end_vote_list = VoteDetail.objects.filter(vote=end_vote).order_by('-vote_cnt')

        if end_vote_list != None:
            max_vote = end_vote_list[0].vote_cnt
            onset_list = [v for v in end_vote_list if v.vote_cnt == max_vote]

        return render(request, 'book_club/club_detail.html',
                      {'book_club': book_club,
                       'bookclub_id': bookclub_id_json,
                       'vote': vote,
                       'vote_id': vote_id_json,
                       'book_info': book,
                       'book_list': book_list,
                       'book_id': book_id_json,
                       'user_list': user_list,
                       'is_owner': is_owner,
                       'is_member': is_member,
                       'user_id': user_id_json,
                       'is_full_json': is_full_json,
                       'end_vote': end_vote,
                       'end_vote_list': end_vote_list,
                       'onset_list': onset_list,
                       'check': check})

    except BookClubVote.DoesNotExist:
        return render(request, 'book_club/club_detail.html',
                      {'book_club': book_club, 'bookclub_id': bookclub_id_json,
                       'book_info': book,
                       'book_list': book_list,
                       'book_id': book_id_json,
                       'user_list': user_list,
                       'is_owner': is_owner,
                       'is_member': is_member,
                       'user_id': user_id_json,
                       'is_full_json': is_full_json})


def book_club_edit(request, bookclub_id):
    if request.method == "GET":
        book_club = get_object_or_404(BookClub, pk=bookclub_id)
        bookclub_id_json = json.dumps(book_club.id)

        query = Q()
        query.add(Q(club=book_club), query.AND)
        query.add(Q(type="OWNER") | Q(type="MEMBER"), query.AND)

        member_list = BookClubMember.objects.prefetch_related("user").filter(query)
        user_list = [member.user for member in member_list]
        category = json.dumps(book_club.category)
        image = json.dumps(book_club.image)
        return render(request, 'book_club/club_revise.html', {"book_club": book_club,
                                                              "user_list": user_list,
                                                              "category": category,
                                                              "image": image,
                                                              "bookclub_id": bookclub_id_json})
    elif request.method == "POST":
        book_club = get_object_or_404(BookClub, pk=bookclub_id)

        book_club.club_name = request.POST["clubname"]
        book_club.image = request.POST["club_img"]
        book_club.category = request.POST["book_category"]
        book_club.description = request.POST["content"]
        book_club.zoom_link = request.POST["zoom_link"]
        book_club.kakao_link = request.POST["kakao_link"]
        book_club.save()

        return redirect('book_club:book_club_detail', book_club.id)

    elif request.method == "DELETE":
        book_club = get_object_or_404(BookClub, pk=bookclub_id)
        book_club.delete()
        return JsonResponse({"message": "소모임 삭제 성공.",
                             }, json_dumps_params={'ensure_ascii': False}, status=200)


def get_book_club_image(request):
    if request.method == 'GET':
        page = request.GET.get("page")

        response = {}
        base_src = "../../static/img/club_img_"
        last_src = ".jpg"
        response['image'] = []
        response['nums'] = []

        if page == "1":
            for i in range(1, 5):
                response['image'].append(base_src + str(i) + last_src)
                response['nums'].append(i)
        elif page == "2":
            for i in range(5, 9):
                response['image'].append(base_src + str(i) + last_src)
                response['nums'].append(i)
        elif page == "3":
            for i in range(9, 13):
                response['image'].append(base_src + str(i) + last_src)
                response['nums'].append(i)

        return JsonResponse(response, status=200)


def get_book(bookclub_id):
    return Book.objects.filter(club_id=bookclub_id, active=False).order_by('-created_at')[0:5]


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
            club.score += 5
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


class member_reject(View):
    def get(self, request):
        clubId = request.GET.get('clubId', None)
        book_club = get_object_or_404(BookClub, id=clubId)

        members = getMember(book_club)
        return render(request, 'book_club/member_reject.html',
                      {'members': members, 'book_club': book_club})

    def patch(self, request):
        req = json.loads(request.body)
        memberId = req['memberId']
        type = "REJECT"
        member = get_object_or_404(BookClubMember, pk=memberId)
        club = member.club

        member.type = type
        member.save()

        total, curr_cnt = member.get_club_cnt()

        if curr_cnt > 0 and type == "REJECT":
            club.decrement_member_cnt()
            club.save()

            club_response = {'clubName': club.club_name,
                             'memberCnt': club.member_cnt,
                             'maxCnt': club.member_total
                             }

            member_response = {'nickname': member.user.nickname,
                               'type': member.type}

            return JsonResponse({'member': member_response,
                                 'club': club_response,
                                 "message": "멤버 내보내기 성공"})
        else:
            return JsonResponse({'message': "잘못된 접근 입니다.",
                                 }, json_dumps_params={'ensure_ascii': False}, status=400)


def response_accept(request):
    if request.method == "PATCH":
        req = json.loads(request.body)
        type = req["type"]
        book_club_id = req["clubId"]
        user = request.user
        club = get_object_or_404(BookClub, pk=book_club_id)
        member = BookClubMember.objects.get(user=user, club=club)

        if member.type != "INVITE":
            return JsonResponse({'message': "초대된 멤버가 아닙니다.",
                                 }, json_dumps_params={'ensure_ascii': False}, status=404)

        member.type = type
        if type == "MEMBER":
            club.score += 5
        member.save()
        club.save()

        return JsonResponse({'message': "멤버 상태 변경 성공", "member": member.type
                             }, json_dumps_params={'ensure_ascii': False}, status=200)


class Invite(View):
    #TODO
    def get(self, request):
        club_list = BookClub.objects.filter(owner=request.user)

        if request.GET.get('userId'):
            user_id = request.GET.get['userId']
            target_user = get_object_or_404(pk=user_id)
            return render(request, "book_club/club_invite.html", {"club_list": club_list, 'target_user': target_user})

        return render(request, "book_club/club_invite.html", {"club_list": club_list})

    def post(self, request):
        value = request.POST["club"]
        return render(request, "book_club/club_invite.html")


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
    elif request.method == "DELETE":
        req = json.loads(request.body)
        bookclub_id = req['bookClubId']
        user_id = req['userId']

        try:
            find_member = BookClubMember.objects.get(club_id=bookclub_id, user_id=user_id)
            find_member.delete()
            return JsonResponse({'message': "멤버 삭제 성공",
                                 }, json_dumps_params={'ensure_ascii': False}, status=200)
        except:
            print("존재하지 하지 않는 멤버입니다.")
            return JsonResponse({'message': "존재하지 하지 않는 멤버입니다.",
                                 }, json_dumps_params={'ensure_ascii': False}, status=400)


class VoteRequest(View):
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
        vote.active = True

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

    def patch(self, request):
        req = json.loads(request.body)
        id = req['voteId']
        vote = get_object_or_404(BookClubVote, pk=id)

        vote.active = False
        vote.save()

        return JsonResponse({"description": "투표가 종료 되었습니다.",
                             }, json_dumps_params={'ensure_ascii': False}, status=200)

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

        query = Q()
        query.add(Q(user_id=request.user.id), query.AND)
        query.add(Q(type="OWNER") | Q(type="MEMBER"), query.AND)
        query.add(Q(club=club), query.AND)

        if not BookClubMember.objects.filter(query).exists():
            # TODO: 권한 없음 에러페이지 헨들링
            return HttpResponse("멤버가 아님", status=403)

        return render(request, 'book_club/vote.html', {'vote': vote, 'voteList': voteList})

    def post(self, request):
        vote_detail_id = request.POST['vote']
        vote_detail = VoteDetail.objects.get(id=vote_detail_id)
        vote_detail.vote_cnt += 1
        vote_detail.save()

        vote = BookClubVote.objects.get(id=vote_detail.vote_id)

        check = VoteCheck()
        check.user = request.user
        check.vote = vote
        check.checked = True
        check.save()

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

    def patch(self, request):
        req = json.loads(request.body)
        book_id = req["bookId"]

        find_book = Book.objects.get(id=book_id, active=True)
        find_book.active = False
        find_book.save()

        response = {"img": find_book.book_img,
                    "message": "현재 책이 책장으로 옮겨졌습니다."}

        return JsonResponse(response, json_dumps_params={'ensure_ascii': False},
                            status=200)


def getBookClub():
    literature = BookClub.objects.filter(category="문학").order_by('-created_at')[0:3]
    humanities = BookClub.objects.filter(category="인문").order_by('-created_at')[0:3]
    self_development = BookClub.objects.filter(category="자기계발").order_by('-created_at')[0:3]
    political_society = BookClub.objects.filter(category="정치/사회").order_by('-created_at')[0:3]
    art = BookClub.objects.filter(category="예술").order_by('-created_at')[0:3]
    science = BookClub.objects.filter(category="과학").order_by('-created_at')[0:3]
    it = BookClub.objects.filter(category="기술/IT").order_by('-created_at')[0:3]
    amity = BookClub.objects.filter(category="자율").order_by('-created_at')[0:3]
    popular = BookClub.objects.filter().order_by('-score')[0:3]

    book_club = {
        'popular': popular,
        'literature': literature,
        'humanities': humanities,
        'self_development': self_development,
        'political_society': political_society,
        'art': art,
        'science': science,
        'it': it,
        'amity': amity
    }

    return book_club


def getMember(book_club):
    query = Q()
    query.add(Q(club=book_club), query.AND)
    query.add(Q(type="MEMBER"), query.AND)

    return BookClubMember.objects.filter(query)


def recommend_member(request):
    user = request.user
    recommend = User.objects.filter(categories=user.categories).exclude(id=user.id).order_by('?')[:3]
    return recommend


# videochat

def room(request, bookclub_id):
    initial_user = request.user
    user_nickname = json.dumps(initial_user.nickname)
    return render(request, 'book_club/room.html', {'user_nickname': user_nickname})


def getToken(request):
    appId = "d4703ab33e584e8eb8e9db094e0745f0"
    appCertificate = "61976e9ab7ee47d4b243401a35b5d898"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
