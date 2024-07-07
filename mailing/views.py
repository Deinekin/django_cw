from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect
from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing


class Home(TemplateView):
    template_name = 'mailing/base.html'


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.all()


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    # model = Client
    form_class = ClientForm
    # fields = ('email', 'name')
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy('mailing:view_all_clients')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    # model = Client
    # fields = ('email', 'name')
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy('mailing:view_all_clients')

    def get_queryset(self):
        return Client.objects.all()


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client

    success_url = reverse_lazy('mailing:view_all_clients')


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.all()


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy('mailing:view_all_messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy('mailing:view_all_messages')

    def get_queryset(self):
        return Message.objects.all()


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message

    success_url = reverse_lazy('mailing:view_all_messages')


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        return Mailing.objects.all()


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    permission_required = "mailing.can_view_mailings"


class MailingCreateView(LoginRequiredMixin, CreateView):
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    # fields = ('start_time', 'end_time', 'period', 'status')
    success_url = reverse_lazy('mailing:view_all_mailings')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy('mailing:view_all_mailings')

    def get_queryset(self):
        return Mailing.objects.all()


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing

    success_url = reverse_lazy('mailing:view_all_mailings')


def change_mailing_status(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    if mailing.status == "S":
        mailing.status = "C"
    mailing.save()
    return redirect(reverse('mailing:view_all_mailings'))
