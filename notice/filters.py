from django.contrib.auth.models import User
from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Notice


def notices(request):
    if request is None:
        return Notice.objects.none()

    notice = Notice.objects.filter(author=request.user)
    return notice

class MessageFilter(FilterSet):
    notice = ModelChoiceFilter(
        field_name='notice',
        queryset=notices,
        label='Title',
        empty_label='All'
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        label='From',
        empty_label='All'
    )

    date = DateFilter(
        field_name='date_in',
        widget=DateInput(attrs={'type': 'date'}),
        label='Date, from',
        lookup_expr='date__gt'
    )
