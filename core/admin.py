from django.contrib import admin
from .models import *
# from core.models import Profile, Post, # ...

# admin.site.register(Post)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'likes', 'creator', 'status']
    list_filter = ['status', 'creator']
    search_fields = [
        'name', 'description', 'status',
        'creator__username', 'creator__first_name'
    ]
    list_editable = ['name', 'status']

    inlines = [CommentInline]

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Short)
admin.site.register(SavedPosts)
admin.site.register(Notification)
