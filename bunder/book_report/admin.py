from django.contrib import admin
from .models import BookReport
# Register your models here.


# Register your models here.
class BookReportAdmin(admin.ModelAdmin):
    fields = ['book_name', 'book_author', 'category', 'content']

admin.site.register(BookReport, BookReportAdmin)