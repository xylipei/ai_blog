from django import template

register = template.Library()


@register.simple_tag
def nav_link_active(item, request):
    if item.link_type != 'internal':
        return ''
    u = (item.url or '/').strip()
    if not u.startswith('/'):
        u = '/' + u
    path = request.path
    if u.rstrip('/') == '' or u == '/':
        return 'active' if path == '/' else ''
    base = u.rstrip('/')
    if path.rstrip('/') == base:
        return 'active'
    return ''
