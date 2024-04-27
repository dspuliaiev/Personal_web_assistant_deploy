from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .models import Contact
from .forms import ContactForm



class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/create.html'
    success_url = reverse_lazy('main')


class ContactSearchResultsView(ListView):
    model = Contact
    template_name = 'contacts/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Contact.objects.filter(name__icontains=query)
        return Contact.objects.all()


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/update.html'
    success_url = reverse_lazy('main')


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contacts/delete.html'
    success_url = reverse_lazy('main')


class BirthdayContactsListView(ListView):
    model = Contact
    template_name = 'contacts/birthday_list.html'

    def get_queryset(self):
        current_date = timezone.now().date()
        days_ahead = 7  # Задана кількість днів
        return Contact.objects.filter(
            birthday__gte=current_date,
            birthday__lte=current_date + timedelta(days=days_ahead))
