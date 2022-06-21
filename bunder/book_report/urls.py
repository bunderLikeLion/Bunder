from django.urls import path
from . import views

app_name = 'book_report'

urlpatterns = [
    path('write_report/', views.write_report),
]