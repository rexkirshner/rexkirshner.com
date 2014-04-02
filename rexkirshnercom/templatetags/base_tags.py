from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if request.path.startswith(pattern):
        return 'active'
    return request.path + ' ' + pattern