from django import forms
from .models import News

from ckeditor.widgets import CKEditorWidget


class NewsForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = News
        fields = [
            'title',
            'text',
        ]
