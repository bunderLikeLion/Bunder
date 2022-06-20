from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'password', 'age', 'nickname', 'categories']

admin.site.register(User, UserAdmin)
