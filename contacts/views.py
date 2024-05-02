from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView
from .forms import ContactForm
from .models import Contact


class IndexView(TemplateView):
    template_name = 'contacts/index.html'

class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/list.html'
    context_object_name = 'list'
    paginate_by = 10

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/create.html'
    success_url = reverse_lazy('contacts:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/update.html'
    success_url = reverse_lazy('contacts:list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/delete.html'
    success_url = reverse_lazy('contacts:list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ContactSearchResultsView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/search.html'
    context_object_name = 'contacts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Contact.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(additional_data__icontains=query) |
                Q(birthday__icontains=query),
                user=self.request.user
            )
        return Contact.objects.filter(user=self.request.user)



class ContactUpcomingBirthdayListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/birthdays.html'
    context_object_name = 'birthdays'

    def get_queryset(self):
        queryset = Contact.objects.filter(user=self.request.user)
        days_ahead = self.request.GET.get('days_ahead')

        if days_ahead is None or days_ahead == '':
            days_ahead = 1
        else:
            try:
                days_ahead = int(days_ahead)
            except ValueError:
                days_ahead = 1

        today = timezone.now().date()
        target_date = today + timedelta(days=days_ahead)

        queryset = queryset.filter(
            birthday__day=target_date.day,
            birthday__month=target_date.month
        )

        return queryset

