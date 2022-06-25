from django.urls import path, register_converter
from . import views
from . import converters

app_name = 'book_report'

register_converter(converters.HangulSlugConverter, 'slugConverter')

urlpatterns = [
    path('<int:id>', views.detail_report, name = "detail"),
    path('write', views.write_report, name = "new"),
    path('create', views.create, name = "create"),
    path('update/<int:id>', views.update, name = 'update'),
    path('edit/<int:id>', views.edit, name = "edit"),
    path('delete/<int:id>', views.delete, name = "delete"),
    path('main', views.main, name = "main"),
    path('category/<slugConverter:category>', views.category_search, name = "category_search"),
    path('search', views.search, name = "search"),
    path('scrap', views.make_scrap, name='make_scrap'),
    path('myscrap', views.all_my_scraps.as_view(), name = 'all_my_scrap'),
    path('like/', views.likes, name = "likes"),
    path('comment', views.CreateComment.as_view()),
    # path('<int:book_report_id>/comment/<int:comments_id>/delete', views.comment_delete, name = 'comment_delete'),
]