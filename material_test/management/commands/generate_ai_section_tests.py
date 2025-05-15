# material_test/management/commands/generate_ai_section_tests.py

import os
import re
import openai

from django.core.management.base import BaseCommand, CommandError
from material.models import Section, Theory
from material_test.models import Test, Question, AnswerOption

# Создаём клиента OpenAI v1.x
client = openai.OpenAI()

class Command(BaseCommand):
    help = 'Генерирует по 3 вопроса для каждого раздела (или одного, если указан --section_id) с помощью ChatGPT'

    def add_arguments(self, parser):
        parser.add_argument(
            '--section_id',
            type=int,
            help='ID раздела; если не указан — обрабатываются все разделы'
        )

    def handle(self, *args, **options):
        section_id = options.get('section_id')

        if section_id:
            try:
                sections = [Section.objects.get(id=section_id)]
            except Section.DoesNotExist:
                raise CommandError(f"Раздел с id={section_id} не найден")
        else:
            sections = Section.objects.all()

        for section in sections:
            theories = Theory.objects.filter(topic__section=section)
            if not theories.exists():
                self.stdout.write(self.style.WARNING(
                    f'⚠ Нет теории для раздела "{section.title}" (ID {section.id})'
                ))
                continue

            theory_text = "\n\n".join(t.content for t in theories if t.content)

            prompt = f"""
Ты преподаватель Python. Сгенерируй 3 вопроса с вариантами ответа (a–d) на основе теории ниже.
Формат:
Вопрос: ...
a) ...
b) ...
c) ...
d) ...
Правильный ответ: <буква>

Теория:
{theory_text}
""".strip()

            self.stdout.write(f"Генерируем вопросы для раздела '{section.title}' (ID {section.id})...")

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                content = response.choices[0].message.content
                questions = self.parse_questions(content)
            except openai.OpenAIError as e:
                raise CommandError(f"Ошибка OpenAI API: {e}")

            if not questions:
                self.stdout.write(self.style.WARNING(
                    f"Не удалось распарсить вопросы"
                ))
                return

            test, _ = Test.objects.get_or_create(
                section=section,
                title=f"ИИ-тест: {section.title}"
            )

            for q in questions:
                question_obj = Question.objects.create(
                    test=test,
                    text=q['question']
                )
                for key in ['a', 'b', 'c', 'd']:
                    AnswerOption.objects.create(
                        question=question_obj,
                        text=q['choices'].get(key, f"Вариант {key.upper()}"),
                        is_correct=(key == q['correct'])
                    )

            self.stdout.write(self.style.SUCCESS(
                f"✅ Раздел '{section.title}' — сгенерировано {len(questions)} вопросов"
            ))

    def parse_questions(self, content):
        """
        Парсит ответ от GPT:
        возвращает список словарей вида
        {
            'question': 'Текст вопроса',
            'choices': {'a': '...', 'b': '...', 'c': '...', 'd': '...'},
            'correct': 'b'
        }
        """
        blocks = re.split(r'Вопрос\s*\d*\s*[:：]', content, flags=re.IGNORECASE)[1:]
        parsed = []

        for block in blocks:
            lines = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
            if len(lines) < 5:
                continue

            q_text = lines[0]
            choices = {}
            correct = None

            for line in lines[1:]:
                m = re.match(r'^([a-dA-D])[\).:]\s*(.+)$', line)
                if m:
                    key, val = m.groups()
                    choices[key.lower()] = val.strip()
                elif 'правильный ответ' in line.lower():
                    cm = re.search(r'([a-dA-D])', line)
                    if cm:
                        correct = cm.group(1).lower()

            if q_text and choices and correct in choices:
                parsed.append({
                    'question': q_text,
                    'choices': choices,
                    'correct': correct
                })

        return parsed
