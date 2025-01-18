from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    Author,
    Book,
)
from datetime import date


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

        labels = {
            'author': _('Author'),
            'title': _('Title'),
            'publisher': _('Publisher'),
            'place': _('Place'),
            'year': _('Year'),
            'category': _('Category')    
        }

    def clean_author_name(self):
        author_name = self.cleaned_data.get("author_name")
        if author_name:
            author, created = Author.objects.get_or_create(name=author_name)
            self.cleaned_data['author'] = author
        return author_name

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year:
            year_value = year.name
            if year_value > date.today().year or year_value < 0:
                raise forms.ValidationError("Not a valid year")
        return year
