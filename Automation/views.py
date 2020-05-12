from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log
from .forms import hostnamecisco, vlan_cisco, ospf_cisco, ciscobackup
from django.contrib import messages
from django.db.models.fields.related import ManyToManyField
#from djansible.models import PlayBooks
from itertools import chain
from dj_ansible.models import AnsibleNetworkHost, AnsibleNetworkGroup
from dj_ansible.ansible_kit import execute
import json
from datetime import datetime
#from djansible.ansible_kit.executor import execute


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
    all_device = AnsibleNetworkHost.objects.all()
    context = {
        'all_device': len(all_device)
    }
    return render(request, 'ansibleweb/home.html', context)

def devices(request):
    all_device = AnsibleNetworkHost.objects.all()
    all_group = AnsibleNetworkGroup.objects.all()

    context = {
        'all_device': all_device,
        'all_group': all_group
    }
    return render(request, 'ansibleweb/device.html', context)

def updategroup(request, pk):
    group = AnsibleNetworkGroup.objects.get(id=pk)
    form = PostInventoryGroup(instance=group)

    if request.method == 'POST':
        form = PostInventoryGroup(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'ansibleweb/post_group.html', context)


def updatedevice(request, pk):
    device = AnsibleNetworkHost.objects.get(id=pk)
    form = PostInventoryHost(instance=device)
    
    if request.method == 'POST':
        form = PostInventoryHost(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'ansibleweb/post_host.html',context)

def deletegroup(request, id):
    group = AnsibleNetworkGroup.objects.get(pk=id)
    group.delete()
    return redirect('device')

def deletedevice(request, id):
    device = AnsibleNetworkHost.objects.get(pk=id)
    device.delete()
    return redirect('device')


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

def addPlaybook(request):
    if request.method == 'POST':
        p_form = PostPlayBookForm(request.POST)
        t_form = TaskForm(request.POST)
        if p_form.is_valid() and t_form.is_valid():
            tasks = t_form.save()
            playbook = p_form.save(commit=False)
            playbook.task = tasks
            playbook.save()
            messages.success(request, f'Your playbook has been created!')
            print(request.POST)
            data = request.POST
            my_play = dict(
                name=data['name'],
                hosts=data['hosts'],
                become=data['become'],
                become_method=data['become_method'],
                gather_facts=data['gather_facts'],
                tasks=[
                    dict(action=dict(module=data['module'], commands=data['commands']))
                    ]
                ) 
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'p_form': p_form,
                't_form': t_form,
                'output': output
            }
            return render(request, 'ansibleweb/post_playbook.html', context)
            #return redirect('Ansible-home')
    else:
        p_form = PostPlayBookForm()
        t_form = TaskForm()
    
    context = {
        'p_form': p_form,
        't_form': t_form
    }
    
    return render(request, 'ansibleweb/post_playbook.html', context)

def addTask(request):
    if request.method == 'POST':
        p_form = PostPlayBookForm(request.POST)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Task hasbeen created!')
            return redirect('Ansible-home')
    else:
        p_form = PostPlayBookForm()

    context = {
        'p_form': p_form
    }

    return render(request, 'ansibleweb/post_playbook.html',context)

def namecisco(request):
    if request.method == 'POST':
        host_form = hostnamecisco(request.POST)
        if host_form.is_valid():
            host_form.save()
            messages.success(request, f'Configure Hostname Success')
            print(request.POST)
            data = request.POST
            #host = form.cleaned_data.get['hosts']
            #name = form.cleaned_data.get['hostname']
            my_play = dict(
                name="hostname",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_config', lines=data['name']))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'host_form': host_form,
                'output': output
            }
            return render(request, 'ansibleweb/ciscohostname.html', context)
    else:
        host_form = hostnamecisco()
    
    context = {
        'host_form': host_form
    }
    return render(request, 'ansibleweb/ciscohostname.html', context)

def vlancisco(request):
    if request.method == 'POST':
        vlan = vlan_cisco(request.POST)
        if vlan.is_valid():
            #host = form.cleaned_data.get('hosts')
			#id = form.cleaned_data.get('vlan_id')
            #name = form.cleaned_data.get('vlan_name')
            print(request.POST)
            data = request.POST
            #host = form.cleaned_data['hosts']
            #name = form.cleaned_data['hostname']
            my_play = dict(
                name="hostname",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_vlan', vlan_id=data['vlan_id'], name=data['vlan_name']))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'vlan': vlan,
                'output': output
            }
            return render(request, 'ansibleweb/ciscovlan.html', context)
    else:
        vlan = vlan_cisco()
    
    context = {
        'vlan': vlan
    }
    return render(request, 'ansibleweb/ciscovlan.html', context)

def ospfcisco(request):
    if request.method == 'POST':
        ospf = ospf_cisco(request.POST)
        if ospf.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="hostname",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_config', lines=data['lines'], parents=data['parents']))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'ospf': ospf,
                'output': output
            }
            return render(request, 'ansibleweb/ciscoospf.html', context)
    else:
        ospf = ospf_cisco()
    
    context = {
        'ospf': ospf
    }
    return render(request, 'ansibleweb/ciscoospf.html', context)

def play():
    plays = PlayBooks.objects.all().prefetch_related('task')
    
    my_play = [{
        'name':play.name,
        'hosts':play.hosts, 
        'become':play.become, 
        'become_method':play.become_method, 
        'gather_facts':play.gather_facts, 
        'tasks':[{'module':actions.module, 'commands':actions.commands} for actions in play.task.all()]} for play in plays]

def log(request):
    logs = log.objects.all()

    context = {
        'logs': logs
    }
    return render(request, 'ansibleweb/home.html', context)

# INI BENAR BACKUP

def backupcisco(request):
    if request.method == 'POST':
        backup = ciscobackup(request.POST)
        if backup.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="nyihuy",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_config', backup='yes'), register='output'),
                    dict(action=dict(module='copy', src="{{output.backup_path}}", dest="/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config")),
                    dict(action=dict(module='lineinfile', path="/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config", line="Building configuration...", state='absent')),
                    dict(action=dict(module='lineinfile', path="/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config", regexp="Current configuration.*", state='absent'))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'backup': backup,
                'output': output
            }
            return render(request, 'ansibleweb/ciscobackup.html', context)
    else:
        backup = ciscobackup()
    
    context = {
        'backup': backup
    }
    return render(request, 'ansibleweb/ciscobackup.html', context)

