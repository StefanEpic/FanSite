from django.contrib import admin
from .models import Category, Notice, Message

from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Notice


class NoticeAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Notice
        fields = '__all__'


class NoticeAdmin(admin.ModelAdmin):
    form = NoticeAdminForm


admin.site.register(Notice, NoticeAdmin)

admin.site.register(Category)
admin.site.register(Message)
