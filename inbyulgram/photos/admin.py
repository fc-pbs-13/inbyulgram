from django.contrib import admin

from photos.models import Photo, Comment


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'caption', 'posted_at', 'user']


admin.site.register(Photo, PhotoAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'user', 'description', 'commented_at']


admin.site.register(Comment, CommentAdmin)
