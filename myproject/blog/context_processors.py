from django.db.models import Count, Q

from .models import NavLink, Category, Post, SiteProfile, Tag


def blog_sidebar(request):
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-created_on')[:5]
    nav_links = NavLink.objects.filter(
        placement=NavLink.PLACEMENT_HEADER,
        is_active=True,
    ).order_by('order', 'id')
    footer_links = NavLink.objects.filter(
        placement=NavLink.PLACEMENT_FOOTER,
        is_active=True,
    ).order_by('order', 'id')
    site_profile = SiteProfile.objects.first()
    tags_sidebar = (
        Tag.objects.annotate(
            published_count=Count('posts', filter=Q(posts__status='published')),
        )
        .filter(published_count__gt=0)
        .order_by('-published_count', 'name')[:24]
    )
    return {
        'categories': categories,
        'recent_posts': recent_posts,
        'nav_links': nav_links,
        'footer_links': footer_links,
        'site_profile': site_profile,
        'tags_sidebar': tags_sidebar,
    }
