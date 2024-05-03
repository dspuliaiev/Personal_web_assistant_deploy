
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Note, Tag
from .forms import NoteForm
from django.db import transaction

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        # Фильтруем заметки, чтобы показывать только заметки текущего пользователя
        return Note.objects.filter(user=self.request.user)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note_list')

    def get_form_kwargs(self):
        # Удалите отправку 'user', если он не используется в форме
        kwargs = super(NoteCreateView, self).get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NoteCreateView, self).form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note_list')

    def get_queryset(self):
        # Пользователь может редактировать только свои заметки
        return super().get_queryset().filter(user=self.request.user)

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:note_list')

    def get_queryset(self):
        # Пользователь может удалять только свои заметки
        return super().get_queryset().filter(user=self.request.user)
