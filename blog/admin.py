from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'publication_sign', 'number_of_views')
    list_filter = ('publication_sign',)
    search_fields = ('title', 'content')
