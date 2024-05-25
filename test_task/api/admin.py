from django.contrib import admin
from .models import ApiUser, Section, UserSection
# Register your models here.

admin.site.register(ApiUser)
admin.site.register(Section)
admin.site.register(UserSection)