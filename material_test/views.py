from material.models import Language
from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, AnswerOption
from material_test.models import TestProgress
from django.contrib.auth.decorators import login_required

def language_list(request):
    languages = Language.objects.all()
    return render(request, 'test/language_list.html', {'languages': languages})

def tests_by_language(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    tests = Test.objects.filter(section__language=language).distinct()

    passed_tests = request.session.get('passed_tests', [])

    return render(request, 'test/tests_by_language.html', {
        'language': language,
        'tests': tests,
        'passed_tests': passed_tests,
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, AnswerOption

def test_start(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = list(test.question_set.all())

    if not questions:
        return render(request, 'test/test_start.html', {
            'test': test,
            'message': "Нет вопросов в этом тесте."
        })

    # Инициализация сессии
    if 'question_index' not in request.session or request.session.get('test_id') != test.id:
        request.session['question_index'] = 0
        request.session['test_id'] = test.id
        request.session['correct_count'] = 0

    index = request.session['question_index']
    total_questions = len(questions)

    # Завершение теста
    if index >= total_questions:
        correct_count = request.session.get('correct_count', 0)

        # Сохраняем в список пройденных тестов
        passed_tests = request.session.get('passed_tests', [])
        if test.id not in passed_tests:
            passed_tests.append(test.id)
            request.session['passed_tests'] = passed_tests

        # Очищаем текущий прогресс
        request.session.pop('question_index', None)
        request.session.pop('test_id', None)
        request.session.pop('correct_count', None)

        return render(request, 'test/test_start.html', {
            'test': test,
            'finished': True,
            'correct_count': correct_count,
            'total_questions': total_questions,
        })

    # Отображение текущего вопроса
    question = questions[index]
    answers = question.answeroption_set.all()
    incorrect = False

    # Обработка ответа
    if request.method == 'POST':
        selected_id = int(request.POST.get('answer'))
        selected_answer = get_object_or_404(AnswerOption, id=selected_id)
        # Сохраняем результат только если пользователь залогинен
        if request.user.is_authenticated:
            TestProgress.objects.create(
                user=request.user,
                test=test,
                question=question,
                is_correct=selected_answer.is_correct
            )

        if selected_answer.is_correct:
            request.session['correct_count'] += 1
            request.session['question_index'] += 1
            return redirect('test_start', test_id=test.id)
        else:
            incorrect = True  # остаёмся на этом же вопросе

    return render(request, 'test/test_start.html', {
        'test': test,
        'question': question,
        'answers': answers,
        'incorrect': incorrect,
        'question_index': index,
        'total_questions': total_questions,
    })
