from django.contrib.auth.models import User
from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Notice, Message


class MessageFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(MessageFilter, self).__init__(*args, **kwargs)
        self.filters['notice'].queryset = Notice.objects.filter(author=kwargs['request'],
                                                                message__status=True).distinct()
        self.filters['author'].queryset = User.objects.filter(message__notice__author=kwargs['request']).distinct()

    notice = ModelChoiceFilter(
        field_name='notice',
        queryset='notice',
        label='Title',
        empty_label='All'
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset='author',
        label='From',
        empty_label='All'
    )

    date = DateFilter(
        field_name='date_in',
        widget=DateInput(attrs={'type': 'date'}),
        label='Date, from',
        lookup_expr='date__gt'
    )

    class Meta:
        model = Message
        fields = ('notice', 'author', 'date')
