from django import template

register = template.Library()

@register.filter
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)