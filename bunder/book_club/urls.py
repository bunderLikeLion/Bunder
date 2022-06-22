from django.urls import path
from . import views

app_name = 'book_club'

urlpatterns = [
    path('new/', views.new, name="new"),
    path('<int:bookclub_id>', views.book_club_detail, name='book_club_detail'),
]