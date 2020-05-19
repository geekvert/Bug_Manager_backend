from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Bug)
admin.site.register(Comment)
