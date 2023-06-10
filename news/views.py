from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import News, Subscribers
from .utils import TestIsModerator


class NewsList(ListView):
    model = News
    ordering = ['-date_in']
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_moderator'] = self.request.user.groups.filter(name='Moderators').exists()
        context['is_subscriber'] = Subscribers.objects.filter(user=self.request.user).exists()
        print(context['is_subscriber'])
        return context


class NewsCreate(LoginRequiredMixin, TestIsModerator, CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.author = self.request.user
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, TestIsModerator, UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')


class NewsDelete(LoginRequiredMixin, TestIsModerator, DeleteView):
    model = News
    success_url = reverse_lazy('news_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@login_required
def subscribe_news(request):
    user = request.user
    if not Subscribers.objects.filter(user=user).exists():
        Subscribers.objects.create(user=user)
    return redirect(reverse_lazy('news_list'))


@login_required
def unsubscribe_news(request):
    user = request.user
    Subscribers.objects.filter(user=user).delete()
    return redirect(reverse_lazy('news_list'))
