from django.contrib import admin
from .models import *
# from core.models import Profile, Post, # ...

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Short)
admin.site.register(SavedPosts)
admin.site.register(Notification)
