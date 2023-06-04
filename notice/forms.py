from django import forms
from .models import Notice

from ckeditor.widgets import CKEditorWidget


class NoticeForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Notice
        fields = [
            'category',
            'title',
            'text',
        ]
