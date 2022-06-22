from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

from .models import BookClub


@csrf_exempt
def new(request):
    if request.method == "GET":
        return render(request, 'book_club/add_club.html')
    elif request.method == "POST":

        book_club = BookClub()
        book_club.owner = request.user
        book_club.club_name = request.POST["clubname"]
        book_club.member_cnt = request.POST["number_of_member"]
        book_club.image = request.POST["club_img"]
        book_club.category = request.POST["book_club_category"]
        book_club.description = request.POST["description"]
        # print("request.data: ",request.POST)

        if request.POST.get('zoom_url', True):
            book_club.link = request.POST["zoom_url"]

        book_club.save()
        return redirect('/bookclub/' + str(book_club.id))


def book_club_detail(request, bookclub_id):
    book_club = get_object_or_404(BookClub, id=bookclub_id)

    return render(request, 'book_club/club_detail.html', {'book_club' : book_club})