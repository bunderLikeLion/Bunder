from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.views import View
import json
from .models import BookClub, BookClubVote, VoteDetail, BookClubMember


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
        book_club.category = request.POST["book_club_category"]
        book_club.description = request.POST["description"]
        book_club.save()

        member, created = BookClubMember.objects.get_or_create(
            club=get_object_or_404(BookClub, id=book_club.id),
            user=request.user,
            type=BookClubMember.type_enum[2][0]  # 소모임장
        )

        if request.POST.get('zoom_url', True):
            book_club.link = request.POST["zoom_url"]

        return redirect('/bookclub/' + str(book_club.id))


def book_club_detail(request, bookclub_id):
    book_club = get_object_or_404(BookClub, id=bookclub_id)
    bookclub_id_json = json.dumps(book_club.id)
    return render(request, 'book_club/club_detail.html', {'book_club': book_club, 'bookclub_id': bookclub_id_json})


class club_admit(View):
    def get(self, request):
        clubId = request.GET.get('clubId', None)
        members = BookClubMember.objects.filter(club_id=clubId)
        book_club = get_object_or_404(BookClub, id=clubId)
        return render(request, 'book_club/club_admit.html',
                      {'members': members, 'book_club': book_club})


@csrf_exempt
def request_member(request):
    req = json.loads(request.body)
    bookclub_id = req['id']
    if request.method == "POST":
        member, created = BookClubMember.objects.get_or_create(
            club=get_object_or_404(BookClub, id=bookclub_id),
            user=request.user,
        )

        return JsonResponse({'member': model_to_dict(member)})


class AddVote(View):
    def get(self, request):
        clubId = request.GET.get('clubId', None)
        club = BookClub.objects.get(id=clubId)

        if club.owner_id != request.user:
            # TODO: 권한 없음 에러페이지 헨들링
            return redirect("/")
        return render(request, 'book_club/add_vote.html')

    def post(self, request):
        clubId = request.GET.get('clubId', None)
        club = BookClub.objects.get(id=clubId)

        if club.owner_id != request.user:
            # TODO: 권한 없음 에러페이지 헨들링
            return redirect("/")

        vote_list = request.POST.getlist('input[]')

        vote = BookClubVote()
        vote.club = club
        vote.topic = request.POST['topic']
        vote.start_date = request.POST['startvote']
        vote.end_date = request.POST['endvote']

        vote.save()

        for each_vote in vote_list:
            vote_detail = VoteDetail()
            vote_detail.description = each_vote
            vote_detail.vote = vote
            vote_detail.save()

        return render(request, 'book_club/add_vote.html')


class Vote(View):

    def get(self, request):
        clubId = request.GET.get('clubId', None)
        voteId = request.GET.get('voteId', None)
        club = BookClub.objects.get(id=clubId)
        vote = BookClubVote.objects.get(id=voteId)

        if club.owner_id != request.user:
            # TODO: 권한 없음 에러페이지 헨들링
            return redirect("/")

        return render(request, 'book_club/add_vote.html')
