from django.shortcuts import render

def index(request):
    return render(request, 'index_old.html')


def archive_material(request):
    return render(request, 'archive_material.html')

def main_material(request):
    return render(request, 'main_material.html')

from django.shortcuts import render
from .models import Language, Section, Topic, Theory

def theory_view(request):
    selected_lang = request.GET.get("lang")
    selected_section = request.GET.get("section")
    selected_topic = request.GET.get("topic")

    languages = Language.objects.all()
    sections = Section.objects.filter(language_id=selected_lang) if selected_lang else None
    topics = Topic.objects.filter(section_id=selected_section) if selected_section else None
    theories = Theory.objects.filter(topic_id=selected_topic) if selected_topic else None

    context = {
        "languages": languages,
        "sections": sections,
        "topics": topics,
        "theories": theories,
        "selected_lang": selected_lang,
        "selected_section": selected_section,
        "selected_topic": selected_topic,
    }
    return render(request, "main_material.html", context)
