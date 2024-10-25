from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.core.serializers import serialize


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            group.members.add(request.user)
            messages.success(request, 'Group created successfully!')
            return redirect('group_list')
    else:
        form = GroupForm()
    
    return render(request, 'chat/create_group.html', {'form': form})

@login_required
def group_list(request):
    user_groups = Group.objects.filter(members=request.user)
    available_groups = Group.objects.exclude(members=request.user)
    
    context = {
        'user_groups': user_groups,
        'available_groups': available_groups
    }
    return render(request, 'chat/group_list.html', context)

@login_required
def update_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, created_by=request.user)
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group updated successfully!')
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    
    return render(request, 'chat/update_group.html', {'form': form, 'group': group})

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, created_by=request.user)
    
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully!')
        return redirect('group_list')
    
    return render(request, 'chat/delete_group.html', {'group': group})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if request.user not in group.members.all():
        group.members.add(request.user)
        messages.success(request, f'You have joined {group.name}!')
    
    return redirect('group_list')

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if request.user in group.members.all() and request.user != group.created_by:
        group.members.remove(request.user)
        messages.success(request, f'You have left {group.name}')
    
    return redirect('group_list')


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        return redirect('group_list')
    
    members = group.members.all().order_by('username')
    messages = group.messages.all().select_related('sender').order_by('timestamp')
    attachment_form = ChatAttachmentForm()
    
    if request.method == 'POST':
        content = request.POST.get('message')
        message = None
        
        if content:
            message = GroupChat.objects.create(
                group=group,
                sender=request.user,
                content=content
            )
            
        if request.FILES.get('file'):
            attachment_form = ChatAttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.uploaded_by = request.user
                attachment.group_chat = message
                attachment.save()
                
        return redirect('group_detail', group_id=group_id)
    
    context = {
        'group': group,
        'members': members,
        'messages': messages,
        'attachment_form': attachment_form,
    }
    return render(request, 'chat/group_detail.html', context)


@login_required
def get_messages(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    last_message_id = request.GET.get('last_message_id')
    messages_query = group.messages.all()
    
    if last_message_id:
        messages_query = messages_query.filter(id__gt=last_message_id)
    
    messages_data = []
    for msg in messages_query:
        message_data = {
            'id': msg.id,
            'content': msg.content,
            'sender_username': msg.sender.username,
            'timestamp': msg.timestamp.strftime('%b %d, %Y %I:%M %p'),
            'attachment': msg.chatattachment_set.first().file.url if msg.chatattachment_set.exists() else None
        }
        messages_data.append(message_data)
    
    return JsonResponse({'messages': messages_data})



@login_required
@require_POST
def send_message(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    content = request.POST.get('message', '').strip()
    attachment = request.FILES.get('file')
    
    message = GroupChat.objects.create(
        group=group,
        sender=request.user,
        content=content or "Shared an attachment"
    )
    
    if attachment:
        ChatAttachment.objects.create(
            file=attachment,
            group_chat=message,
            uploaded_by=request.user
        )
        
    return JsonResponse({
        'status': 'success',
        'message_id': message.id,
        'attachment_url': message.chatattachment_set.first().file.url if attachment else None
    })


@login_required
def send_attachment(request):
    if request.method == 'POST':
        form = ChatAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.uploaded_by = request.user
            attachment.private_chat = PrivateChat.objects.create(
                sender=request.user,
                receiver_id=request.POST.get('receiver_id'),
                content=f"Sent an attachment: {request.FILES['file'].name}"
            )
            attachment.save()
            
            return JsonResponse({
                'status': 'success',
                'attachment': {
                    'url': attachment.file.url,
                    'filename': attachment.file.name,
                    'timestamp': attachment.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
    return JsonResponse({'status': 'error'})


@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)
    selected_user_id = request.GET.get('user_id')
    selected_user = None
    messages = []
    
    if selected_user_id:
        selected_user = get_object_or_404(User, id=selected_user_id)
        messages = PrivateChat.objects.filter(
            models.Q(sender=request.user, receiver=selected_user) |
            models.Q(sender=selected_user, receiver=request.user)
        ).order_by('timestamp')
        
        # Mark messages as read
        messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    context = {
        'users': users,
        'selected_user': selected_user,
        'messages': messages,
    }
    
    return render(request, 'chat/chat_layout.html', context)

@login_required
def send_private_message(request):
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=request.POST.get('receiver_id'))
        content = request.POST.get('message').strip()
        
        if content:
            message = PrivateChat.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )
            
            return JsonResponse({
                'status': 'success',
                'message': {
                    'content': message.content,
                    'sender': message.sender.username,
                    'timestamp': message.timestamp.strftime('%I:%M %p')
                }
            })
    
    return JsonResponse({'status': 'error'})

@login_required
def get_messages(request):
    user_id = request.GET.get('user_id')
    other_user = get_object_or_404(User, id=user_id)
    
    messages = PrivateChat.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    messages_data = [{
        'content': msg.content,
        'sender': msg.sender.username,
        'timestamp': msg.timestamp.strftime('%I:%M %p')
    } for msg in messages]
    
    return JsonResponse({'messages': messages_data})


