import openai
import re
from django.core.management.base import BaseCommand
from material.models import Section, Theory
from material_test.models import Test, Question, AnswerOption

openai.api_key = 'your-openai-key-here'  # 🔐 вставь свой ключ

class Command(BaseCommand):
    help = 'Генерирует 10 вопросов по каждому разделу с помощью ChatGPT'

    def handle(self, *args, **kwargs):
        sections = Section.objects.all()

        for section in sections:
            theories = Theory.objects.filter(topic__section=section)
            if not theories.exists():
                self.stdout.write(self.style.WARNING(f'Нет теории для раздела "{section.title}"'))
                continue

            theory_text = "\n".join(t.text for t in theories)
            prompt = f"""
Ты преподаватель Python. Сгенерируй 10 вопросов с вариантами ответа (a–d) на основе теории ниже.
Формат:
Вопрос: ...
a) ...
b) ...
c) ...
d) ...
Правильный ответ: <буква>

Теория:
{theory_text}
"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )

            content = response['choices'][0]['message']['content']
            questions = self.parse_questions(content)

            if not questions:
                self.stdout.write(self.style.WARNING(f"Не удалось распарсить вопросы для раздела '{section.title}'"))
                continue

            test, _ = Test.objects.get_or_create(section=section, title=f"ИИ-тест: {section.title}")

            for q in questions:
                question_obj = Question.objects.create(test=test, text=q['question'])
                for key in ['a', 'b', 'c', 'd']:
                    AnswerOption.objects.create(
                        question=question_obj,
                        text=q['choices'].get(key, f"Вариант {key.upper()}"),
                        is_correct=(key == q['correct'])
                    )

            self.stdout.write(self.style.SUCCESS(f"✅ Раздел '{section.title}' — сгенерировано {len(questions)} вопросов"))

    def parse_questions(self, content):
        """Парсит GPT-ответ: возвращает список словарей вопросов"""
        blocks = re.split(r'Вопрос\s*[:：]', content)[1:]  # разбиваем по "Вопрос:"
        parsed = []

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 5:
                continue

            q_text = lines[0].strip()
            choices = {}
            correct = None

            for line in lines[1:]:
                line = line.strip()
                match = re.match(r'^([a-dA-D])[\).:]\s*(.+)$', line)
                if match:
                    key, val = match.groups()
                    choices[key.lower()] = val.strip()
                elif 'правильный ответ' in line.lower():
                    correct_match = re.search(r'([a-dA-D])', line)
                    if correct_match:
                        correct = correct_match.group(1).lower()

            if q_text and choices and correct in choices:
                parsed.append({
                    'question': q_text,
                    'choices': choices,
                    'correct': correct
                })

        return parsed
#python manage.py generate_ai_section_tests
