from django import forms
from django.contrib import admin
from markdownx.widgets import MarkdownxWidget

from .models import Post, Category, Comment, NavLink, Tag, SiteProfile

# Django Admin 站点标题（与 LANGUAGE_CODE=zh-hans 配合，内置界面为简体中文）
admin.site.site_header = '博客管理后台'
admin.site.site_title = '博客'
admin.site.index_title = '站点管理'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    verbose_name = '评论'
    verbose_name_plural = '评论'


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': MarkdownxWidget(
                attrs={
                    'data-markdownx-editor-max-height': '480',
                    'data-markdownx-preview-max-height': '480',
                }
            ),
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'slug', 'author', 'created_on', 'status', 'category')
    list_editable = ('status',)
    list_filter = ('status', 'created_on', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)
    # 不使用 date_hierarchy：MySQL 未加载时区表时，USE_TZ=True 会触发
    # ValueError: Database returned an invalid datetime value...
    inlines = [CommentInline]
    save_on_top = True
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'status', 'category', 'tags'),
        }),
        ('正文（Markdown）', {
            'fields': ('content',),
            'description': '支持 Markdown，侧栏实时预览；编辑器内可拖拽/粘贴图片上传（需登录后台）。',
        }),
        ('展示与摘要', {
            'fields': ('featured_image', 'excerpt'),
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    @admin.action(description='通过所选评论')
    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display = ('label', 'url', 'link_type', 'placement', 'order', 'is_active', 'open_in_new_tab')
    list_filter = ('placement', 'link_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('label', 'url')


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'author_display_name', 'icp_number')
    fieldsets = (
        ('基本信息', {
            'fields': ('site_name', 'tagline', 'author_display_name'),
        }),
        ('关于页与侧栏', {
            'fields': ('about_sidebar', 'about_page_html'),
        }),
        ('社交与联系', {
            'fields': ('github_url', 'twitter_url', 'bilibili_url', 'email'),
        }),
        ('页脚备案', {
            'fields': ('icp_number', 'icp_url'),
            'description': '备案号显示在网站底部；链接一般为 https://beian.miit.gov.cn/ 或主办单位提供的公示地址，可留空。',
        }),
    )

    def has_add_permission(self, request):
        if SiteProfile.objects.exists():
            return False
        return super().has_add_permission(request)
