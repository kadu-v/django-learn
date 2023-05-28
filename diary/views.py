from typing import Any, Optional
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from .forms import DiaryCreateForm, InquiryForm
import logging
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Diary
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin

logger = logging.getLogger(__name__)


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self) -> bool | None:
        diary = get_object_or_404(Diary, pk=self.kwargs["pk"])  # type: ignore
        return self.request == diary.user  # type: ignore


class IndexView(OnlyYouMixin, generic.TemplateView):
    template_name = "index.html"


class InquiryView(OnlyYouMixin, generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form: InquiryForm) -> HttpResponse:
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました')
        logger.info('Inquary sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class DiaryListView(LoginRequiredMixin, OnlyYouMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        diaries = Diary.objects.filter(
            user=self.request.user).order_by('-created_at')
        return diaries


class DiaryDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'


class DiaryCreateView(LoginRequiredMixin,  generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)


class DiaryUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の更新に失敗しました。')
        return super().form_invalid(form)


class DiaryDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        messages.success(self.request, "日記を削除しました。")
        return super().form_valid(form)  # type: ignore
