from django.contrib import admin
from .models import Post, Comment, Announcements, Members

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Announcements)
admin.site.register(Members)
