from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import Textarea, TextInput

from django.db import models
from django.utils.text import format_lazy

from .models import Type, Skill, CharacterClass, SkillAlias


class SkillAliasInline(admin.TabularInline):
    model = SkillAlias
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 50, 'rows': 2, 'placeholder': 'Flavor text on class'})},
        models.CharField: {'widget': TextInput(attrs={'placeholder': 'Name on class'})}
    }
    classes = ['collapse']


@admin.register(SkillAlias)
class SkillAliasAdmin(admin.ModelAdmin):
    list_display = ('alias_name', 'skill', 'character_class')
    search_fields = ('skill', 'alias_name')
    fieldsets = [
        (
            None,
            {
                'fields': ['alias_name', ('skill', 'character_class')]
            },
        ),
        (
            'More Options',
            {
                'classes': ['collapse',],
                'fields': ['alias_description']
            }
        )
    ]

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'skill':
    #         kwargs['queryset'] = Skill.objects.filter(classes__icontains=db_field.name)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    autocomplete_fields = ('types',)
    fieldsets = [
        (
            'Basic Information',
            {
                'fields': ['name', ('cost', 'category', 'types')]
            },
        ),
        (
            'Rules Text',
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
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # if db_field.name == 'skills':
        kwargs['widget'] = FilteredSelectMultiple('Skills', False)
        # else:
        #     return super().formfield_for_manytomany(db_field, request, **kwargs)
        # if 'queryset' not in kwargs:
        #     if db_field.name == 'skills':
        #         queryset = Skill.objects.all()
        #         if queryset is not None:
        #             kwargs['queryset'] = queryset
        #     else:
        #         queryset = Skill.objects.all()
        #         if queryset is not None:
        #             kwargs['queryset'] = queryset

    search_fields = ('name',)
    fields = [('name', 'body_points'), 'description']
    inlines = [SkillAliasInline]


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
