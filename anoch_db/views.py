from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from anoch_db.models import Skill, CharacterClass
from .forms import SearchBar


def index(request):
    class_list = CharacterClass.objects.order_by('name')
    context = {'class_list': class_list, }
    return render(request, 'anoch_db/index.html', context)


def skill(request, skill_id):
    s = get_object_or_404(Skill, pk=skill_id)
    return render(request, 'anoch_db/skill.html', {'skill': s})


def character_class(request, class_id):
    c = get_object_or_404(CharacterClass, pk=class_id)
    sl = c.skills
    al = sl.through.objects.all()
    aliases = dict(zip(sl.all(), al))
    context = {
        'class': c,
        'skill_dict': aliases
    }
    return render(request, 'anoch_db/class.html', context)


def search_advanced(request):
    form = SearchBar()
    return render(request, 'anoch_db/search_adv.html', {'form': form})


class SearchResultsView(ListView):
    model = Skill
    template_name = 'anoch_db/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Skill.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
