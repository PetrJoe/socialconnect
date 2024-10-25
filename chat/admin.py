from django.contrib import admin
from .models import Group, GroupChat, PrivateChat, ChatAttachment

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('members',)

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group', 'content', 'timestamp')
    list_filter = ('group', 'sender')
    search_fields = ('content',)

@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'is_read')
    list_filter = ('sender', 'receiver', 'is_read')
    search_fields = ('content',)

@admin.register(ChatAttachment)
class ChatAttachmentAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'uploaded_at', 'group_chat', 'private_chat')
    list_filter = ('uploaded_by', 'uploaded_at')
