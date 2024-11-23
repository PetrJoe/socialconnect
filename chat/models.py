from django.db import models
from accounts.models import User
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups')  # Changed from 'groups' to 'chat_groups'
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    
    def __str__(self):
        return self.name

class GroupChat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f'{self.sender.username} in {self.group.name}: {self.content[:50]}'

class PrivateChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.content[:50]}'

class ChatAttachment(models.Model):
    file = models.FileField(upload_to='chat_attachments/')
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, null=True, blank=True)
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Attachment by {self.uploaded_by.username} at {self.uploaded_at}'



class SharedFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='shared_files/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    file_size = models.PositiveIntegerField(editable=False, null=True)
    file_type = models.CharField(max_length=100, editable=False, null=True)
    download_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Shared File'
        verbose_name_plural = 'Shared Files'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('file-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            # Get file type from the file name extension
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)

    def increment_downloads(self):
        self.download_count += 1
        self.save()



