from django.shortcuts import render, get_object_or_404, redirect
from .models import ProgrammingLanguage, Chapter, SubChapter, TestQuestion, TestProgress
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

def test_list(request):
    languages = ProgrammingLanguage.objects.all()
    return render(request, 'archive_test/test_list.html', {'languages': languages})


@login_required
def test_detail(request, language):
    lang = get_object_or_404(ProgrammingLanguage, slug=language)
    chapters = Chapter.objects.filter(language=lang).prefetch_related(
        Prefetch('subchapter_set', queryset=SubChapter.objects.prefetch_related('testquestion_set'))
    )

    question_id = request.GET.get('q')
    questions = TestQuestion.objects.filter(sub_chapter__chapter__language=lang)
    question_list = list(questions)
    total_questions = len(question_list)

    if not question_id:
        return redirect(request.path + f'?q={question_list[0].id}')

    try:
        current_question = TestQuestion.objects.get(id=question_id)
    except TestQuestion.DoesNotExist:
        return redirect(request.path + f'?q={question_list[0].id}')

    progress_qs = TestProgress.objects.filter(user=request.user, question__in=question_list)
    progress_dict = {p.question_id: p.is_correct for p in progress_qs}
    progress_ids = [p.question_id for p in progress_qs]

    # Проверка ответа
    feedback = None
    selected_answer = None
    test_completed = len(progress_dict) == total_questions

    if request.method == 'POST' and not test_completed and current_question.id not in progress_ids:
        selected_answer = request.POST.get('answer')
        if selected_answer:
            is_correct = selected_answer == current_question.correct_answer
            TestProgress.objects.create(
                user=request.user,
                question=current_question,
                selected_answer=selected_answer,
                is_correct=is_correct
            )
            feedback = 'correct' if is_correct else 'incorrect'
    else:
        existing = TestProgress.objects.filter(user=request.user, question=current_question).first()
        if existing:
            selected_answer = existing.selected_answer
            feedback = 'correct' if existing.is_correct else 'incorrect'

    correct_count = sum(progress_dict.values())
    percent_correct = round((correct_count / total_questions) * 100) if total_questions else 0

    current_index = question_list.index(current_question)
    previous_id = question_list[current_index - 1].id if current_index > 0 else None
    next_id = question_list[current_index + 1].id if current_index < total_questions - 1 else None
    current_chapter_id = current_question.sub_chapter.chapter.id

    return render(request, 'archive_test/test_detail.html', {
        'language': lang,
        'chapters': chapters,
        'question': current_question,
        'question_number': question_list.index(current_question) + 1,
        'total_questions': total_questions,
        'selected_answer': selected_answer,
        'feedback': feedback,
        'progress_dict': progress_dict,
        'correct_count': correct_count,
        'percent_correct': percent_correct,
        'current_question_id': current_question.id,
        'test_completed': test_completed,
        'previous_id': previous_id,
        'next_id': next_id,
        'current_chapter_id': current_chapter_id,
    })