from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import *


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


class SkillList(forms.ModelForm):
    class Meta:
        model = CharacterClass
        fields = ['name', 'body_points', 'description', 'skills']
        widgets = {
            'skills': FilteredSelectMultiple(verbose_name='Skills', is_stacked=False)
        }
