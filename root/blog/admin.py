from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)  # to see Model in Admin
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'author', 'created', 'updated', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}  # auto generated
    raw_id_fields = ('author',)  # displayed lookup field instead of dropdown
    date_hierarchy = 'publish'  # adds navigation links by dates o
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
