from django.urls import path
from .views import (
    BirthdayContactsListView,
    ContactSearchResultsView,
    ContactUpdateView,
    ContactDeleteView,
    ContactCreateView,
    main,
    edit
)

app_name = 'contacts'

urlpatterns = [
    path('', main, name='main'),
    path('edit/', edit, name='edit'),
    path('contacts/search/', ContactSearchResultsView.as_view(), name='contact-search'),
    path('contacts/update/<pk>', ContactUpdateView.as_view(), name='contact-update'),
    path('contacts/delete/<pk>', ContactDeleteView.as_view(), name='contact-delete'),
    path('contacts/create/', ContactCreateView.as_view(), name='contact-create'),
    path('contacts/birthdays/', BirthdayContactsListView.as_view(), name='birthday-contacts'),
]