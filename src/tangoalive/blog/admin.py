from django.contrib import admin
from .models import Blog, BlogAdmin
from .models import Tag, TagAdmin
from .models import Author, AuthorAdmin

admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Author, AuthorAdmin)
