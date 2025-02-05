from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    Author,
    Book,
)
from datetime import date
from dal import autocomplete

class BookForm(forms.ModelForm):

    
    class Meta:
        model = Book
        fields = [
            'author',
            'title',
            'publisher',
            'place',
            'year',
            'category',
        ]

        widgets = {
            'author': autocomplete.ModelSelect2Multiple(url='books:author-autocomplete'),
            'category': forms.CheckboxSelectMultiple(),
        }

        labels = {
            'author': _('Author'),
            'title': _('Title'),
            'publisher': _('Publisher'),
            'place': _('Place'),
            'year': _('Year'),
            'category': _('Category')    
        }

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year:
            year_value = year.name
            if year_value > date.today().year or year_value < 0:
                raise forms.ValidationError(_("Not a valid year"))
        return year
