from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django.contrib.admin import widgets, SimpleListFilter, RelatedOnlyFieldListFilter
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import Textarea, TextInput

from django.db import models
from django.utils.text import format_lazy

from .forms import CharacterClassForm
from .models import (Type, SkillDomain, SkillOptions, ClassOptions, Effect,
                     Skill, PeriodicSkill, PassiveSkill, SlotSkill, ExaltedSkill, PrestigePoint, UniqueMechanic,
                     CharacterClass, ClassSkills, SkillAlias,
                     EquipmentType, Component, Material, Consumable, Ritual)


# <editor-fold desc="Inlines">
class AliasListInline(admin.StackedInline):
    model = ClassSkills
    can_delete = False
    show_change_link = True
    extra = 0
    classes = ['collapse']

    fields = ['character_class', 'alias', 'prerequisites']
    readonly_fields = ('character_class',)
    autocomplete_fields = ('prerequisites',)

    verbose_name = 'alias'
    verbose_name_plural = 'aliases'
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


class ClassFilter(admin.SimpleListFilter):
    title = 'class'
    parameter_name = 'class'

    def lookups(self, request, model_admin):
        return [

        ]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(class__contains=self.value())
# </editor-fold>


# <editor-fold desc="Rules Admins">
@admin.register(Skill)
class SkillAdmin(PolymorphicParentModelAdmin):
    base_model = Skill
    child_models = (PeriodicSkill, PassiveSkill, SlotSkill, ExaltedSkill, PrestigePoint, UniqueMechanic)
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = (PolymorphicChildModelFilter,)


@admin.register(PeriodicSkill, UniqueMechanic)
class BasicSkillAdmin(PolymorphicChildModelAdmin):
    base_model = Skill
    autocomplete_fields = ('types',)
    list_display = ('name',)
    search_fields = ('name',)
    base_fieldsets = (
        ('INFO', {"fields": [('name', 'cost'), 'types']}),
        ('RULES TEXT', {"fields": [('description', 'mechanics')]}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 60, 'rows': 4})}
    }
    inlines = [AliasListInline]


@admin.register(PassiveSkill)
class PassiveSkillAdmin(BasicSkillAdmin):
    fieldsets = (
        *BasicSkillAdmin.base_fieldsets,
        ('PASSIVE SKILL DATA', {"fields": ['ability_type']}),
    )


@admin.register(SlotSkill)
class SlotSkillAdmin(BasicSkillAdmin):
    autocomplete_fields = BasicSkillAdmin.autocomplete_fields + ('domain',)
    list_display = BasicSkillAdmin.list_display + ('ability_type', 'rank')
    list_filter = ('ability_type', 'rank')
    fieldsets = (
        *BasicSkillAdmin.base_fieldsets,
        ('SLOT SKILL DATA', {"fields": [('ability_type', 'rank'), 'domain']}),
    )


@admin.register(ExaltedSkill)
class ExaltedSkillAdmin(BasicSkillAdmin):
    list_display = BasicSkillAdmin.list_display + ('exalted_type', 'criteria_type')
    list_filter = ('exalted_type', 'criteria_type')
    fieldsets = (
        *BasicSkillAdmin.base_fieldsets,
        ('EXALTED SKILL DATA', {"fields": ['exalted_type', ('criteria', 'criteria_type')]}),
    )


@admin.register(PrestigePoint)
class PrestigePointAdmin(BasicSkillAdmin):
    autocomplete_fields = BasicSkillAdmin.autocomplete_fields + ('options',)
    search_fields = BasicSkillAdmin.search_fields + ('name',)
    fieldsets = (
        *BasicSkillAdmin.base_fieldsets,
        ('PRESTIGE POINT DATA', {"fields": ['max_purchases', 'options']}),
    )
# </editor-fold>


# <editor-fold desc="Classes">
@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    form = CharacterClassForm
    search_fields = ('name',)
    fieldsets = (
        ('INFO', {"fields": [('name', 'body_points'), 'class_type', 'description']}),
        ('CLASS OPTIONS', {"fields": ['class_options_help', 'class_options'], "classes": ['collapse']}),
        ('SKILLS', {"fields": ['class_skills']})
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.skills.set(form.cleaned_data['class_skills'])


@admin.register(ClassSkills)
class ClassSkillsAdmin(admin.ModelAdmin):
    list_display = ('skill', 'character_class', 'alias')
    list_select_related = ('character_class', 'alias')
    search_fields = ('skill', 'alias')
    autocomplete_fields = ('skill', 'character_class')
    fields = [('skill', 'character_class'), 'alias']

    def has_module_permission(self, request):
        return False
# </editor-fold>


# <editor-fold desc="Rules Options">
@admin.register(SkillAlias)
class SkillAliasAdmin(admin.ModelAdmin):
    list_display = ('alias_name', 'parent_skill', 'parent_class')
    search_fields = ('alias_name', 'parent_skill__name', 'class_skill__character_class')
    list_filter = ['parent_skill', ('class_skill__character_class', RelatedOnlyFieldListFilter)]
    autocomplete_fields = ('alias_domain', 'parent_skill')


@admin.register(ClassOptions)
class ClassOptionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'classes')
    search_fields = ('name',)
    list_filter = [ClassOptionsFilter, 'character_classes']

    @staticmethod
    def classes(obj):
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


@admin.register(Type, SkillOptions, SkillDomain)
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

