from django.db import models
from dj_ansible.models import AnsibleNetworkHost,AnsibleNetworkGroup
from django.forms import ModelForm ,CheckboxInput, ModelChoiceField
from django import forms
from .playbook import Actions, PlayBook
# Create your models here.

#class MyModelChoiceField(ModelChoiceField):
#    def label_from_instance(self, obj):
#        return "My Object #%i" % obj.name
OS_CHOICES =(
    ('ios', 'cisco'),
    ('routeros', 'mikrotik')
)

class PostInventoryGroup(ModelForm):
    ansible_network_os = forms.ChoiceField(choices = OS_CHOICES)
    class Meta:
        model = AnsibleNetworkGroup
        fields = ['name', 'ansible_connection', 'ansible_network_os', 'ansible_become']
        widgets = {
            'name': forms.Textarea(attrs={'cols':100, 'rows':1}),
        #   'ansible_connection': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_network_os': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_become': forms.Textarea(attrs={'cols':100, 'rows':1})
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
    
class PostPlayBookForm(ModelForm):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all(), to_field_name="name")
    class Meta:
        model = PlayBook
        fields = ['name', 'hosts', 'become','become_method','gather_facts']
        exclude = ('task',)
        widgets = {
            'name': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'become': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'become_method': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'gather_facts': forms.Textarea(attrs={'cols':100, 'rows':1})
        }

class TaskForm(ModelForm):
    class Meta:
        model = Actions
        fields = ['module', 'commands']
        widgets = {
            'module': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'commands': forms.Textarea(attrs={'cols':100, 'rows':1})
        }