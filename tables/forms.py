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

        widgets = {
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

    def clean_title(self):
        title = self.cleaned_data.get('title')
        authors = self.cleaned_data.get('author')

        if title and authors:
            existing_books = Book.objects.filter(title__iexact=title)
            for book in existing_books:
                if book.author.filter(id__in=[author.id for author in authors]).exists():
                    raise forms.ValidationError(_("A book with the title already exists for one of the selected authors."))
        
        return title

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year:
            year_value = year.name
            if year_value > date.today().year or year_value < 0:
                raise forms.ValidationError(_("Not a valid year"))
        return year
