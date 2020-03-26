from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import PostInventoryGroup, PostInventoryHost
from django.contrib import messages


# Create your views here.
# skaoksoaksoakas

posts = [
    {
        'author': 'Broto',
        'title': 'Ansible Post 1',
        'content': 'First post content',
        'date_posted': 'Maret 11, 2018'
    },
    {
        'author': 'Indra',
        'title': 'Ansible Post 2',
        'content': 'First post content',
        'date_posted': 'Maret 13, 2018'
    }

]
@login_required
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'ansibleweb/home.html', context)


def about(request):
    return render(request, 'ansibleweb/about.html', {'title': 'About'})


def addgroup(request):
    if request.method == 'POST':
        adddgroup = PostInventoryGroup(request.POST)
        if adddgroup.is_valid():
            adddgroup.save()
            messages.success(request, f'Berhasil membuat group host network')
            return redirect('group-create')
    else:
        adddgroup = PostInventoryGroup()
        return render(request, 'ansibleweb/post_group.html', {'form': adddgroup })

def addhost(request):
    if request.method == 'POST':
        adddhost = PostInventoryHost(request.POST)
        if adddhost.is_valid():
            adddhost.save()
            messages.success(request, f'Berhasil membuat inventory host network')
            return redirect('Ansible-home')
        else:
            return render(request, 'ansibleweb/post_host.html', {'form':adddhost})
    else:
        adddhost = PostInventoryHost()
        return render(request, 'ansibleweb/post_host.html', {'form':adddhost})




