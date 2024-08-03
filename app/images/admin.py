from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')
    list_display_links = ('id', 'title')
    list_filter = ('created',)
