from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientUpdateView, ClientListView,
                           MailingCreateView, MailingDeleteView, MailingDetailView, MailingUpdateView, MailingListView,
                           MessageListView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView,
                           Home, change_mailing_status)

app_name = MailingConfig.name

urlpatterns = [
    path('', Home.as_view(), name='homepage'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('clients/', ClientListView.as_view(), name='view_all_clients'),
    path('client-<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('messages/', MessageListView.as_view(), name='view_all_messages'),
    path('messages-<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('messages/edit/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/', MailingListView.as_view(), name='view_all_mailings'),
    path('mailings-<int:pk>/', MailingDetailView.as_view(), name='view_mailing'),
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailings/change-status/<int:pk>/', change_mailing_status, name='change-status'),
]
