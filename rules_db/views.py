import django.apps
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from rules_db.models import Skill, CharacterClass, RulesChapter, RulesArticle, ClassSkills
from .forms import SearchBar


def index(request):
    class_list = CharacterClass.objects.order_by('name')
    contents_list = RulesChapter.objects.order_by('chapter_number')
    context = {'class_list': class_list, 'contents_list': contents_list, }
    return render(request, 'rules_db/index.html', context)


def sidenav(request):
    contents_list = RulesChapter.objects.all
    context = {'contents_list': contents_list, }
    return render(request, 'rules_db/sidebar.html', context)


def chapter(request, slug):
    chap = get_object_or_404(RulesChapter, slug=slug)
    context = {'chapter': chap, 'contents': chap.get_contents(), 'slug': slug, }
    return render(request, 'rules_db/chapter.html', context)


def rules_article(request, chapter_slug, article_slug):
    chap = get_object_or_404(RulesChapter, slug=chapter_slug)
    article = get_object_or_404(RulesArticle, slug=article_slug)
    context = {'chapter': chap, 'article': article, }
    return render(request, 'rules_db/rules_article.html', context)


def skill(request, skill_id):
    s = get_object_or_404(Skill, pk=skill_id)
    return render(request, 'rules_db/skill.html', {'skill': s})


def character_class(request, class_id):
    c = get_object_or_404(CharacterClass, pk=class_id)
    sl = c.skills
    alias_dict = dict()
    for s in sl.all():
        alias = ClassSkills.objects.get(character_class=class_id, skill=s.id).alias
        if alias is not None:
            alias_dict[s.id] = alias
    context = {
        'character_class': c,
        'alias_dict': alias_dict,
        'skill_dicts': c.get_skills_by_category()
    }
    return render(request, 'rules_db/class.html', context)


def search_advanced(request):
    form = SearchBar()
    return render(request, 'rules_db/search_adv.html', {'form': form})


class SearchResultsView(ListView):
    model = Skill
    template_name = 'rules_db/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Skill.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
