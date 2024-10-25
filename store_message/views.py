from django.shortcuts import render
from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from django.views import generic
from store_message.models import Store
from store_message.forms import StoreForm, EmailLoginForm
import imaplib
from .services import save_account_and_messages, decode_mime_header, parse_date
from datetime import datetime as dt


class StoreListView(generic.ListView):
    model = Store

    def get_context_data(self, **kwargs):
        """ метод для отображения общей информации на главной странице """
        context = super().get_context_data(**kwargs)
        context['stores'] = Store.objects.all()
        return context


class StoreDetailView(generic.DetailView):
    model = Store

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class StoreCreateView(generic.CreateView):
    model = Store
    fields = ('theme', 'description', 'attachment', 'owner',)
    success_url = reverse_lazy('store_message:list')
    form_class = StoreForm

    def form_valid(self, form):
        if form.is_valid():
            new_store = form.save()
            new_store.slug = slugify(new_store.theme)
            new_store.save()
        return super().form_valid(form)


class StoreUpdateView(generic.UpdateView):
    model = Store
    fields = ('theme', 'description', 'attachment', 'owner',)
    form_class = StoreForm

    def form_valid(self, form):
        if form.is_valid():
            new_store = form.save()
            new_store.slug = slugify(new_store.title)
            new_store.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('store_message:view', args=[self.kwargs.get('pk')])


class StoreDeleteView(generic.DeleteView):
    model = Store
    success_url = reverse_lazy('store_message:list')


def email_login(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            mail = imaplib.IMAP4_SSL('imap.yandex.com', 993)
            try:
                mail.login(new_email, password)
                mail.select("inbox")
                result, data = mail.search(None, "ALL")
                mail_ids = data[0]
                id_list = mail_ids.split()
                latest_emails = []
                for i in id_list[-5:]:
                    result, msg_data = mail.fetch(i, '(RFC822)')
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            raw_subject = msg['subject']
                            raw_body = msg['body']
                            raw_from_ = msg['from']
                            raw_date = msg['date']
                            decoded_subject = decode_mime_header(raw_subject)
                            # decoded_body = decode_mime_header(raw_body)
                            decoded_raw_from_ = decode_mime_header(raw_from_)
                            decoded_raw_date = parse_date(raw_date)

                            # Добавляем в список обработанные данные о письме
                            latest_emails.append({
                                'subject': decoded_subject,
                                'body': raw_body,
                                'from': decoded_raw_from_,
                                'date': decoded_raw_date,
                            })


                # for i in id_list[-1:]:
                #     result, msg_data = mail.fetch(i, '(RFC822)')
                #     for response_part in msg_data:
                #         if isinstance(response_part, tuple):
                #             latest_emails.append(response_part[1].decode('utf-8'))
                save_account_and_messages(new_email, password, latest_emails)
                return render(request, 'store_message/store_list.html', {'emails': latest_emails})
            except imaplib.IMAP4.error:
                form.add_error(None, "Неправильные логин или пароль")

    else:
        form = EmailLoginForm()

    return render(request, 'store_message/email_login.html', {'form': form})
