from django import forms
from django.contrib import admin

from photoblog import models

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Location, LocationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Category, CategoryAdmin)

class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_posted'
    list_display = ['id', 'thumbnail', 'title', 'date_posted', 'location', 'flickr_id']
    list_filter = ['date_posted', 'location']
    ordering = ('-date_posted',)
    search_fields = ['title', 'location__name']

    def thumbnail(self, photo):
        return "<img src=\"%s\" />" % photo.thumbnail_url
    thumbnail.allow_tags = True
admin.site.register(models.Photo, PhotoAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Comment, CommentAdmin)

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(models.Page, PageAdmin)
