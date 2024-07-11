from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse

from anoch_db.models import Skill, CharacterClass


# Create your views here.


def index(request):
    class_list = CharacterClass.objects.order_by('name')
    context = {'class_list': class_list, }
    return render(request, 'anoch_db/index.html', context)


def skill(request, skill_id):
    s = get_object_or_404(Skill, pk=skill_id)
    return render(request, 'anoch_db/skill.html', {'skill': s})


def character_class(request, class_id):
    c = get_object_or_404(CharacterClass, pk=class_id)
    return render(request, 'anoch_db/class.html', {'class': c})
