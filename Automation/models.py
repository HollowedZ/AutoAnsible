from django.db import models
from djansible.models import AnsibleNetworkHost,AnsibleNetworkGroup
from django.forms import ModelForm ,CheckboxInput
from django import forms
# Create your models here.


class PostInventoryGroup(ModelForm):
    class Meta:
        model = AnsibleNetworkGroup
        fields = ['name', 'ansible_connection', 'ansible_network_os', 'ansible_become']
        widgets = {
            'name': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_connection': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_network_os': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_become': forms.Textarea(attrs={'cols':100, 'rows':1}),
        }

class PostInventoryHost(ModelForm):
    group = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all())
    class Meta:
        model = AnsibleNetworkHost
        fields = ['host', 'ansible_ssh_host', 'ansible_user', 'ansible_ssh_pass', 'ansible_become_pass', 'group']
        widgets = {
            'host': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_ssh_host': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_user': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_ssh_pass': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_become_pass': forms.Textarea(attrs={'cols':100, 'rows':1})
        }

