from django.contrib import admin
from django.contrib.admin import widgets, SimpleListFilter
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import Textarea, TextInput

from django.db import models
from django.utils.text import format_lazy

from .forms import CharacterClassForm
from .models import (Type, SkillDomain, SkillOptions, ClassOptions, Effect,
                     Skill, PeriodicSkill, PassiveSkill, SlotSkill, ExaltedSkill, PrestigePoint, UniqueMechanic,
                     CharacterClass, ClassSkills,
                     EquipmentType, Component, Material, Consumable, Ritual)


# <editor-fold desc="Inlines">
class SkillAliasInline(admin.TabularInline):
    model = ClassSkills
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
# </editor-fold>


# <editor-fold desc="Search Filters">
class ClassOptionsFilter(admin.SimpleListFilter):
    title = 'keyword'
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        return [('source', 'Source'),
                ('subclass', 'Subclass')]

    def queryset(self, request, queryset):
        if self.value() == 'source':
            return queryset.filter(name__contains="(Source)")
        if self.value() == 'subclass':
            return queryset.filter(name__contains="Subclass")


class SkillOptionFilter(admin.SimpleListFilter):
    pass


class EffectFilter(admin.SimpleListFilter):
    title = 'duration'
    parameter_name = 'duration'

    def lookups(self, request, model_admin):
        return [
            ('na', 'N/A'),
            ('10', '10 sec'),
            ('30', '30 sec'),
            ('60', '1 min'),
            ('300', '5 min'),
            ]

    def queryset(self, request, queryset):
        if self.value() is not None:
            if self.value() == 'na':
                return queryset.filter(duration__exact=-1)
            else:
                return queryset.filter(duration__exact=self.value())
# </editor-fold>


# <editor-fold desc="Rules Admins">
@admin.register(ClassSkills)
class ClassSkillsAdmin(admin.ModelAdmin):
    list_display = ('skill', 'character_class', 'alias')
    list_select_related = ('character_class', 'alias')
    search_fields = ('skill', 'alias')
    autocomplete_fields = ('skill', 'character_class')
    fields = [('skill', 'character_class'), 'alias_name', 'alias_description']

    def has_module_permission(self, request):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    autocomplete_fields = ('types',)
    fieldsets = [
        (
            'BASIC',
            {
                'fields': [('name', 'cost'), 'types']
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
    form = CharacterClassForm
    search_fields = ('name',)
    inlines = [SkillAliasInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'skills' or 'class_options':
            return db_field.formfield(**kwargs)
        else:
            super()
# </editor-fold>


# <editor-fold desc="Rules Options">
@admin.register(ClassOptions)
class ClassOptionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'classes')
    search_fields = ('name', 'character_classes__name')
    list_filter = [ClassOptionsFilter]

    def classes(self, obj):
        return ', '.join([c.name for c in obj.character_classes.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'character_classes'
        )


@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ('name', 'mechanics')
    search_fields = ('name',)
    list_filter = [EffectFilter]
    fieldsets = [
        (
            'BASIC',
            {
                'fields': [('name', 'duration')]
            },
        ),
        (
            'RULES TEXT',
            {
                'fields': [('description', 'mechanics')]
            }
        )
    ]


@admin.register(Type, SkillOptions)
class GeneralOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    fields = ('name', 'description')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    fields = [('name', 'category'), 'description']
    list_filter = ('category',)
# </editor-fold>

