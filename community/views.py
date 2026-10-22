from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import StudyGroup, GroupMessage

@login_required
def community_list(request):
    groups = StudyGroup.objects.all()
    return render(request, 'community/community.html', {'groups': groups})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    return render(request, 'community/group_detail.html', {'group': group})

@login_required
def group_chat(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    if request.user not in group.members.all():
        group.members.add(request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        file = request.FILES.get('file')
        if content or image or file:
            GroupMessage.objects.create(group=group, sender=request.user, content=content, image=image, file=file)
        return redirect('group_chat', group_id=group.id)
    chat_messages = GroupMessage.objects.filter(group=group).order_by('created_at')
    return render(request, 'community/group_chat.html', {'group': group, 'chat_messages': chat_messages, 'members': group.members.all()})

@login_required
def chat_messages_json(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    messages = GroupMessage.objects.filter(group=group).order_by('created_at')
    data = []
    for m in messages:
        data.append({'id': m.id, 'sender': m.sender.username, 'is_me': m.sender == request.user, 'content': m.content, 'image_url': m.image.url if m.image else None, 'file_url': m.file.url if m.file else None, 'file_name': m.file.name.split('/')[-1] if m.file else None, 'time': m.created_at.strftime('%H:%M')})
    return JsonResponse({'messages': data})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    group.members.add(request.user)
    return redirect('group_chat', group_id=group.id)

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    group.members.remove(request.user)
    return redirect('community_list')