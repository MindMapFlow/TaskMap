import csv
from django.core.management.base import BaseCommand
from material.models import Language, Section, Topic, Theory

class Command(BaseCommand):
    help = "Импортирует теории из CSV-файла"

    def handle(self, *args, **kwargs):
        path = "python_theory_50_utf8_bom.csv"  # путь к файлу

        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                lang_name = row['language'].strip()
                section_title = row['section'].strip()
                topic_title = row['topic'].strip()
                content = row['content'].strip()

                # Создаём язык, если нет
                language, _ = Language.objects.get_or_create(name=lang_name)

                # Создаём раздел
                section, _ = Section.objects.get_or_create(language=language, title=section_title)

                # Создаём тему
                topic, _ = Topic.objects.get_or_create(section=section, title=topic_title)

                # Создаём теорию, если ещё нет
                if not Theory.objects.filter(topic=topic).exists():
                    Theory.objects.create(topic=topic, content=content)
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"Импортировано {count} теорий."))
