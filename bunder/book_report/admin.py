from django.contrib import admin
from .models import BookReport, Scrap, Comment
# Register your models here.


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = ['user', 'report_name', 'book_name', 'book_author', 'book_category','book_img', 'content', 'likes', 'image_upload']

admin.site.register(BookReport, BookAdmin)

class ScrapAdmin(admin.ModelAdmin):
    fields = ['user', 'book_report']

admin.site.register(Scrap, ScrapAdmin)

class CommentAdmin(admin.ModelAdmin):
    fields = ['user', 'book_report', 'content', 'created_at']

admin.site.register(Comment, CommentAdmin)