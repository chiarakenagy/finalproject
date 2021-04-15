from django.contrib import admin

from .models import Question, Choice, Profile

admin.site.site_header = "This or That Admin"
admin.site.index_title  = "Welcome to This or That!"

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Profile)


# Register your models here.
