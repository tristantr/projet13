from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Favorite, Comment

User = get_user_model()

admin.site.register(User)
admin.site.register(Favorite)
admin.site.register(Comment)