from django.urls import path
from . import views

app_name = 'book_report'

urlpatterns = [
    path('<int:id>', views.detail_report, name = "detail"),
    path('write_report/', views.write_report, name = "new"),
    path('create/', views.create, name = "create"),
]