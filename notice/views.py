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
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NoticeDetail(DetailView):
    model = Notice
    template_name = 'notice_detail.html'
    context_object_name = 'notice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.path.split('/')[-2]
        notice = Notice.objects.get(id=pk)
        context['is_author'] = (self.request.user == notice.author)
        context['categories'] = Category.objects.all()
        return context


class NoticeCreate(LoginRequiredMixin, CreateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'notice_edit.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NoticeUpdate(LoginRequiredMixin, TestIsAuthorThisNotice, UpdateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'notice_edit.html'
    success_url = reverse_lazy('notice_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
