from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']

    def clean_title(self):
        """ Validate and sanitize the title field to prevent XSS """
        title = self.cleaned_data.get('title')
        if "<script>" in title or "</script>" in title:
            raise forms.ValidationError("Invalid input detected.")
        return title