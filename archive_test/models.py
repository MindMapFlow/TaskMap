from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.number}) {self.title}"

class SubChapter(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.chapter.number}.{self.number}) {self.title}"

class TestQuestion(models.Model):
    sub_chapter = models.ForeignKey(SubChapter, on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    choices = models.JSONField()  # Example: ["A", "B", "C", "D"]

class TestProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=200, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
