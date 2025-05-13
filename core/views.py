from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    return render(request, 'core/index.html')

@login_required
def profile_view(request):
    user = request.user
    progress = TestProgress.objects.filter(user=user).select_related('question__sub_chapter__chapter__language')

    progress_by_lang = {}
    for item in progress:
        lang = item.question.sub_chapter.chapter.language.name
        if lang not in progress_by_lang:
            progress_by_lang[lang] = {'correct': 0, 'total': 0}
        progress_by_lang[lang]['total'] += 1
        if item.is_correct:
            progress_by_lang[lang]['correct'] += 1

    progress_data = []
    for lang, data in progress_by_lang.items():
        percent = round((data['correct'] / data['total']) * 100) if data['total'] > 0 else 0
        progress_data.append({'language': lang, 'total': data['total'], 'correct': data['correct'], 'percent': percent})

    return render(request, 'core/profile.html', {'progress_data': progress_data})
from material_test.models import TestProgress

@login_required
def profile_view(request):
    user = request.user
    progress = TestProgress.objects.filter(user=user).select_related('test__section__language')

    progress_by_lang = {}

    for item in progress:
        lang = item.test.section.language.name
        if lang not in progress_by_lang:
            progress_by_lang[lang] = {'correct': 0, 'total': 0}
        progress_by_lang[lang]['total'] += 1
        if item.is_correct:
            progress_by_lang[lang]['correct'] += 1

    progress_data = []
    for lang, stats in progress_by_lang.items():
        percent = round((stats['correct'] / stats['total']) * 100)
        progress_data.append({
            'language': lang,
            'total': stats['total'],
            'correct': stats['correct'],
            'percent': percent
        })

    return render(request, 'core/profile.html', {'progress_data': progress_data})
