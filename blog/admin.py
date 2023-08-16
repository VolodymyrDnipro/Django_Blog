from django.contrib import admin
from .models import Post, Comment, UserProfile, Notification


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_draft', 'created_at', 'updated_at')
    list_filter = ('is_draft', 'created_at', 'updated_at')
    search_fields = ('title', 'owner__username', 'created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'username', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('post__title', 'username', 'created_at')
    raw_id_fields = ('post',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message', 'created_at')
