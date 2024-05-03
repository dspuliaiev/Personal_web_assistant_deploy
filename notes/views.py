
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Note, Tag
from .forms import NoteForm
from django.db import transaction
from django.db.models import Q

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

from django.views.generic import ListView
from .models import Note, Tag

class NoteSearchView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/notes_search.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        tag_query = self.request.GET.get('tag')
        queryset = Note.objects.filter(user=self.request.user)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        if tag_query:
            queryset = queryset.filter(tags__name__icontains=tag_query)

        return queryset.distinct()
    def get_context_data(self, **kwargs):
        context = super(NoteSearchView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()  # Предполагаем, что теги общедоступны
        return context
