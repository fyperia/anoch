from django import forms


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
