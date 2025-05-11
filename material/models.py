from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Section(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.language.name} — {self.title}"

class Topic(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.section.title} — {self.title}"

class Theory(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True, null=True)  # 👈 вот тут
