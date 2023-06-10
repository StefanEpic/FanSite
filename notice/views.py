from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import NoticeForm, MessageForm
from .models import Notice, Category, Message
from .utils import TestIsAuthorThisNotice
from .filters import MessageFilter


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
    paginate_by = 4

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
    template_name = 'message_create.html'
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


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    ordering = ['-date_in']
    template_name = 'message_list.html'
    context_object_name = 'messages'
    paginate_by = 4

    def get_queryset(self):
        queryset = Message.objects.filter(notice__author=self.request.user, status=True)
        self.filterset = MessageFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['categories'] = Category.objects.all()
        return context


@login_required
def message_delete(request, pk):
    try:
        message = Message.objects.get(id=pk)
        if request.user == message.notice.author:
            message.delete()
            return redirect(reverse_lazy('message_list'))
        return HttpResponseForbidden()
    except:
        return HttpResponseForbidden()


@login_required
def message_apply(request, pk):
    try:
        message = Message.objects.get(id=pk)
        if request.user == message.notice.author:
            message.status = False
            message.save(update_fields=['status'])
            return redirect(reverse_lazy('message_list'))
        return HttpResponseForbidden()
    except:
        return HttpResponseForbidden()
