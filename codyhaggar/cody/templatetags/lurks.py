from django import template

register = template.Library()

@register.filter(name='lurked_by')
def lurked_by(challenge, user):
    return challenge.was_lurked_by(user)

