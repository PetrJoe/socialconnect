from django.urls import path
from .views import *


urlpatterns = [
    path('group/create/', create_group, name='create_group'),
    path('groups/', group_list, name='group_list'),
    path('group/<int:group_id>/update/', update_group, name='update_group'),
    path('group/<int:group_id>/delete/', delete_group, name='delete_group'),
    path('group/<int:group_id>/join/', join_group, name='join_group'),
    path('group/<int:group_id>/leave/', leave_group, name='leave_group'),
    path('group/<int:group_id>/', group_detail, name='group_detail'),
    path('api/messages/<int:group_id>/', get_messages, name='get_messages'),
    path('api/send_message/<int:group_id>/', send_message, name='send_message'),
    path('send-message/', send_private_message, name='send_message'),
    path('send-attachment/', send_attachment, name='send_attachment'),
    path('chat/', chat_view, name='chat'),
    path('get-messages/', get_messages, name='get_messages'),
]


