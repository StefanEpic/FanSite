from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import NoticeForm
from .models import Notice, Category
from .utils import TestIsAuthorThisNotice


class NoticeList(ListView):
    model = Notice
    ordering = ['-date_in']
    template_name = 'notice_list.html'
    context_object_name = 'notices'
    paginate_by = 5


class NoticeDetail(LoginRequiredMixin, DetailView):
    model = Notice
    template_name = 'notice_detail.html'
    context_object_name = 'notice'


class NoticeCreate(LoginRequiredMixin, CreateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'notice_edit.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.author = self.request.user
        return super().form_valid(form)


class NoticeUpdate(LoginRequiredMixin, TestIsAuthorThisNotice, UpdateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'notice_edit.html'
    success_url = reverse_lazy('notice_list')


class NoticeDelete(LoginRequiredMixin, TestIsAuthorThisNotice, DeleteView):
    model = Notice
    success_url = reverse_lazy('notice_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CategoryList(ListView):
    model = Notice
    template_name = 'notice_list.html'
    context_object_name = 'notices'
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Notice.objects.filter(category=self.category).order_by('-date_in')
