from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import NoticeForm, MessageForm
from .models import Notice, Category, Message
from .utils import TestIsAuthorThisNotice


class NoticeList(ListView):
    model = Notice
    ordering = ['-date_in']
    template_name = 'notice_list.html'
    context_object_name = 'notices'
    paginate_by = 5

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
        context['is_author'] = (self.request.user == self.object.author)
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


class MessageCreate(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    model = Message
    template_name = 'message_edit.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.author = self.request.user
        message.notice = Notice.objects.get(pk=self.request.path.split('/')[-3])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class MessageList(ListView):
    model = Message
    ordering = ['-date_in']
    template_name = 'message_list.html'
    # context_object_name = 'messages'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(author=self.request.user)
        context['categories'] = Category.objects.all()
        return context


class MessageApply(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class MessageDelete(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
