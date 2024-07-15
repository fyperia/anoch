from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import Textarea, TextInput

from django.db import models
from django.utils.text import format_lazy

from .forms import SkillList
from .models import Type, Skill, CharacterClass, SkillAlias


class SkillAliasInline(admin.TabularInline):
    model = SkillAlias
    can_delete = False
    autocomplete_fields = ('skill',)
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 50, 'rows': 2, 'placeholder': 'Override RP text'})},
        models.CharField: {'widget': TextInput(attrs={'placeholder': 'Override name'})},
    }
    classes = ['collapse']
    verbose_name = 'skill Alias'
    verbose_name_plural = 'skill Alias List'

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     kwargs['queryset'] = Skill.objects.filter(character_classes__name__exact=self.model)
    #     return db_field.formfield(**kwargs)


@admin.register(SkillAlias)
class SkillAliasAdmin(admin.ModelAdmin):
    list_display = ('alias_name', 'skill', 'character_class')
    search_fields = ('skill', 'alias_name')
    autocomplete_fields = ('skill', 'character_class')
    fields = [('skill', 'character_class'), 'alias_name', 'alias_description']

    def has_module_permission(self, request):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    autocomplete_fields = ('types',)
    fieldsets = [
        (
            'BASIC',
            {
                'fields': ['name', ('cost', 'category', 'types')]
            },
        ),
        (
            'RULES TEXT',
            {
                'fields': [('description', 'mechanics')]
            }
        )
    ]
    inlines = [SkillAliasInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 60, 'rows': 4})}
    }


@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    form = SkillList
    search_fields = ('name',)
    inlines = [SkillAliasInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'skill_list':
            return db_field.formfield(**kwargs)
        else:
            super(self)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
