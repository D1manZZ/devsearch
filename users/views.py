from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import CreateUser, EditProfile, SendMessage
from .models import Profile, Message
from projects.models import Tag


def developers(request):
    search_phrase = ''

    if request.GET.get('search'):
        search_phrase = request.GET.get('search')

    tags_query = Tag.objects.filter(tag__icontains=search_phrase)
    profiles_query = Profile.objects.distinct().filter(Q(name__icontains=search_phrase) |
                                                       Q(short_intro__icontains=search_phrase) |
                                                       Q(skills__in=tags_query))

    context = {'developers': profiles_query, 'search_phrase': search_phrase}
    return render(request, 'users/developers.html', context)


def login_user(request):
    values = {
        'username': '',
        'password': ''
    }
    if request.POST.get('username') and request.POST.get('username'):
        values['username'] = request.POST.get('username')
        values['password'] = request.POST.get('password')
    if request.user.is_authenticated:
        return redirect('projects')
    if request.method == 'POST':
        data = request.POST
        try:
            User.objects.get(username=data['username'])
        except:
            messages.error(request, 'username doesnt exist')
        user = authenticate(request, username=data['username'], password=data['password'])
        if user:
            login(request, user)
            messages.success(request, 'successfully logged in')
            return redirect('profile', pk=user.profile.id)
        else:
            messages.error(request, 'wrong password')
    return render(request, 'users/login.html', {'values': values})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, 'user was successfully logged out')
    return redirect('login')


def register(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            if form.cleaned_data['email'] not in map(lambda x: x['email'], User.objects.all().values('email')):
                print(User.objects.all().values('email'))
                user = form.save()
                login(request, user)
                messages.success(request, 'user was successfully registered')
                return redirect('profile', pk=user.profile.id)
            else:
                messages.error(request, 'Email address already registered')
    return render(request, 'users/register.html', {'form': form})


def profile(request, pk):
    user_profile = Profile.objects.get(pk=pk)
    return render(request, 'users/profile.html', {'profile': user_profile})


@login_required(login_url='login')
def edit_profile(request):
    form = EditProfile(instance=Profile.objects.get(pk=request.user.profile.id))
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=Profile.objects.get(pk=request.user.profile.id))
        if form.is_valid():
            form.save()
            messages.success(request, 'profile was successfully changed')
            return redirect('profile', pk=request.user.profile.id)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required(login_url='login')
def messages_list(request):
    received_messages = request.user.profile.you_receive.values_list('sender', flat=True).all()
    sent_messages = request.user.profile.you_send.values_list('recipient', flat=True).all()
    profiles_list = Profile.objects.filter(Q(id__in=received_messages) |
                                           Q(id__in=sent_messages))

    total_list = []
    for profile_ in profiles_list:
        total_list.append({
            'profile': profile_,
            'last_message': Message.objects.filter(
                Q(sender=request.user.profile) & Q(recipient=Profile.objects.get(pk=profile_.pk)) |
                Q(sender=Profile.objects.get(pk=profile_.pk)) & Q(recipient=request.user.profile)).last(),
            'new_messages': Message.objects.filter(Q(recipient=request.user.profile) &
                                                   Q(sender=Profile.objects.get(pk=profile_.pk)) &
                                                   Q(checked=False)).count
        })

    context = {
        'profiles_list': total_list
    }
    return render(request, 'users/messages.html', context)


@login_required(login_url='login')
def send_message(request, pk):
    if pk == request.user.profile.id:
        return redirect('messages')

    recipient = Profile.objects.get(pk=pk)
    form = SendMessage()
    Message.objects.filter(Q(sender=Profile.objects.get(pk=pk)) &
                           Q(recipient=request.user.profile) &
                           Q(checked=False)).update(checked=True)

    if request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            message_obj = form.save(commit=False)
            message_obj.sender = request.user.profile
            message_obj.recipient = Profile.objects.get(pk=pk)
            message_obj.save()
            messages.success(request, 'your message was successfully send')
            return redirect('send_message', pk=pk)

    messages_obj = Message.objects.filter(Q(sender=request.user.profile) & Q(recipient=Profile.objects.get(pk=pk)) |
                                          Q(sender=Profile.objects.get(pk=pk)) & Q(recipient=request.user.profile))

    context = {
        'recipient': recipient,
        'form': form,
        'messages_obj': messages_obj
    }

    return render(request, 'users/send_message.html', context)
