from django import forms
from .models import Notice, Message

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


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'text',
        ]
