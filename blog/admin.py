from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content")
