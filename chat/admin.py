from django.contrib import admin
from .models import *


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


@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'uploaded_at', 'get_file_size')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('name', 'description', 'user__username')
    date_hierarchy = 'uploaded_at'
    
    def get_file_size(self, obj):
        """Return file size in a human-readable format"""
        size = obj.file.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    get_file_size.short_description = 'File Size'
