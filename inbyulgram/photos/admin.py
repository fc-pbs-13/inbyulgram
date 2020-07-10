from django.contrib import admin

from photos.models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['image', 'caption', 'posted_at', 'user']


admin.site.register(Photo, PhotoAdmin)
