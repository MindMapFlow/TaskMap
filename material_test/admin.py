from django.contrib import admin
from .models import Test, Question, AnswerOption

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4  # сразу 4 варианта
    min_num = 2
    max_num = 6

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'correct_answer_display']
    inlines = [AnswerOptionInline]

    def correct_answer_display(self, obj):
        correct = obj.answeroption_set.filter(is_correct=True).first()
        return correct.text if correct else "❌ Не указан"
    correct_answer_display.short_description = "Правильный ответ"

admin.site.register(Question, QuestionAdmin)
