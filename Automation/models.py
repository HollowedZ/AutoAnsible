from django.db import models
from dj_ansible.models import AnsibleNetworkHost,AnsibleNetworkGroup, devices
from django.forms import ModelForm ,CheckboxInput, ModelChoiceField
from django import forms
from .playbook import Actions, PlayBook
# Create your models here.

#class MyModelChoiceField(ModelChoiceField):
#    def label_from_instance(self, obj):
#        return "My Object #%i" % obj.name
OS_CHOICES =(
    ('ios', 'cisco'),
    ('routeros', 'mikrotik'),
    ('ce', 'huawei')
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

class log(models.Model):
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    messages = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {} - {}".format(self.target, self.action, self.status)

class c_hostname(models.Model):
    name = models.CharField(max_length=255)
    hosts = models.CharField(max_length=255)

class group(forms.Form):
    name = forms.CharField(max_length=255)
    os = forms.ChoiceField(choices = OS_CHOICES)

class addinfodevice(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all())