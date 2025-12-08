from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender,**kwargs):
    if sender.name == 'auth':
        Group.objects.get_or_create(name = 'Student')
        Group.objects.get_or_create(name = 'Teacher')
        Group.objects.get_or_create(name = 'Principal')