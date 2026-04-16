from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify as markdownx_markdownify

register = template.Library()


@register.filter(name='markdownify')
def markdownify(value):
    """与 django-markdownx 后台预览一致的 Markdown→HTML（4.x 已移除 markdownx_tags）。"""
    if value is None or value == '':
        return ''
    return mark_safe(markdownx_markdownify(str(value)))


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
