from django.contrib import admin
from .models import ProgrammingLanguage, Chapter, SubChapter, TestQuestion, TestProgress

admin.site.register(ProgrammingLanguage)
admin.site.register(Chapter)
admin.site.register(SubChapter)
admin.site.register(TestQuestion)
admin.site.register(TestProgress)
