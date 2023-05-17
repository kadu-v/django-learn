from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from .forms import InquiryForm
import logging
from django.urls import reverse_lazy
# Create your views here.

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "index.html"
    

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form: InquiryForm) -> HttpResponse:
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました')
        logger.info('Inquary sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)