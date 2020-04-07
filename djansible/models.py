from django.db import models
from djansible import const

# Create your models here.
class BaseAnsibleGroup(models.Model):
    name = models.CharField(max_length=100)
    ansible_connection = models.CharField(choices=const.ANSIBLE_CONNECTION_CHOICES, max_length=100)

    class Meta:
        abstract = True

class BaseAnsibleDeviceGroup(BaseAnsibleGroup):
    ansible_become = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

class BaseAnsibleHost(models.Model):
    host = models.CharField(max_length=100)
    ansible_ssh_host = models.GenericIPAddressField()
    ansible_user = models.CharField(max_length=100)
    ansible_ssh_pass = models.CharField(max_length=100)

    class Meta:
        abstract = True

class AnsibleNetworkGroup(BaseAnsibleDeviceGroup):
    ansible_network_os = models.CharField(choices=const.ANSIBLE_NETWORK_OS_CHOICES, max_length=100)
    parent_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='child_group', null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        db_table = 'ansible_network_groups'

class AnsibleServerGroup(BaseAnsibleDeviceGroup):
    parent_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='child_group', null=True, blank=True)

    class Meta:
        db_table = 'ansible_server_groups'

class AnsibleAWSGroup(BaseAnsibleGroup):
    ami = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    sshkey = models.CharField(max_length=100)
    vpcid = models.CharField(max_length=100)

    class Meta:
        db_table = 'ansible_aws_groups'

class AnsibleNetworkHost(BaseAnsibleHost):
    ansible_become_pass = models.CharField(max_length=100)
    group = models.ForeignKey(AnsibleNetworkGroup, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ansible_network_hosts'

class AnsibleServerHost(BaseAnsibleHost):
    ansible_become_pass = models.CharField(max_length=100)
    group = models.ForeignKey(AnsibleServerGroup, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ansible_server_hosts'



# MULAI disini ya rippp , ini MODEL buat PUSH CONFIGURASI NYAA


class Actions(models.Model):
    module = models.CharField(max_length=100)
    commands = models.CharField(max_length=100)

    class Meta:
        db_table = 'action'

class PlayBook(models.Model):
    name = models.CharField(max_length=100)
    hosts = models.CharField(max_length=100)
    become = models.CharField(max_length=100)
    become_method = models.CharField(max_length=100)
    gather_facts = models.CharField(max_length=100)
    task = models.ForeignKey(Actions, on_delete=models.DO_NOTHING)
#ini aku cuma nyoba nyoba kalo pake foreign key sm many to many
class PlayBooks(models.Model):
    name = models.CharField(max_length=100)
    hosts = models.CharField(max_length=100)
    become = models.CharField(max_length=100)
    become_method = models.CharField(max_length=100)
    gather_facts = models.CharField(max_length=100)
    task = models.ManyToManyField(Actions)
        

