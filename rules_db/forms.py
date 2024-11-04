from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper

import anochSite
from django.contrib import admin
from .models import CharacterClass, Skill


class SearchBar(forms.Form):
    SEARCH_CHOICES = [
        ('SKL', 'Skills'),
        ('CLS', 'Classes'),
        ('ALL', 'Everything')
    ]
    search_query = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search...'})
    )
    # Ideally, the radio select will be rendered horizontally, but this requires a custom renderer class.
    search_type = forms.ChoiceField(
        label="Search in:", choices=SEARCH_CHOICES, widget=forms.RadioSelect
    )


class CharacterClassForm(forms.ModelForm):
    class Meta:
        model = CharacterClass
        fields = '__all__'
        site = admin.site
        widgets = {
            'class_options': FilteredSelectMultiple(verbose_name='Class Options', is_stacked=False),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['class_skills'].initial = kwargs['instance'].skills.all()

    class_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=RelatedFieldWidgetWrapper(FilteredSelectMultiple("Skills", is_stacked=False),
                                         CharacterClass._meta.get_field('skills').remote_field,
                                         admin.site, can_add_related=True)
    )
