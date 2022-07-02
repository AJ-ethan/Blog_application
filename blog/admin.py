from django.contrib import admin

# Reister your models here.
from blog.models import Post,Comment

#admin.site.register(Post)

@admin.register(Post)#also does the register work
class PostAdmin(admin.ModelAdmin):
	list_display = ('title','slug','author','publish','status')
	list_filter = ('status','created','publish','author')
	search_fields = ('title','body')
	prepopulated_fields = {'slug':('title',)}
	raw_id_fields = ('author',)
	date_hierachy = 'publish'
	ordering = ('status','publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active','created','updated')
	search_fields = ('name', 'email', 'body')
