from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('名称', max_length=100, unique=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('名称', max_length=50, unique=True)
    slug = models.SlugField('URL 别名', max_length=60, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL 别名', max_length=200, unique=True)
    author = models.ForeignKey(
        User,
        verbose_name='作者',
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    content = models.TextField(
        '正文',
        help_text='使用 Markdown 编写；后台使用 django-markdownx 编辑器，可实时预览。',
    )
    featured_image = models.ImageField('特色图片', upload_to='blog/', blank=True, null=True)
    excerpt = models.TextField('摘要', null=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='分类',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True, related_name='posts')
    created_on = models.DateTimeField('发布时间', default=timezone.now)
    updated_on = models.DateTimeField('更新时间', auto_now=True)
    status = models.CharField(
        '状态',
        max_length=10,
        choices=[('draft', '草稿'), ('published', '已发布')],
        default='draft',
    )

    class Meta:
        ordering = ['-created_on']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name='文章',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    name = models.CharField('姓名', max_length=80)
    email = models.EmailField('电子邮箱')
    body = models.TextField('内容')
    created_on = models.DateTimeField('提交时间', auto_now_add=True)
    active = models.BooleanField('已通过审核', default=False)

    class Meta:
        ordering = ['created_on']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'{self.name} 对《{self.post.title}》的评论'


class NavLink(models.Model):
    PLACEMENT_HEADER = 'header'
    PLACEMENT_FOOTER = 'footer'
    PLACEMENT_CHOICES = [
        (PLACEMENT_HEADER, '顶部导航'),
        (PLACEMENT_FOOTER, '页脚链接'),
    ]
    LINK_INTERNAL = 'internal'
    LINK_EXTERNAL = 'external'
    LINK_TYPE_CHOICES = [
        (LINK_INTERNAL, '站内路径'),
        (LINK_EXTERNAL, '外部链接'),
    ]

    label = models.CharField('显示文字', max_length=100)
    url = models.CharField(
        '链接地址',
        max_length=500,
        help_text='站内填写路径，如 /about/；外链写完整地址 https://…',
    )
    link_type = models.CharField(
        '链接类型',
        max_length=10,
        choices=LINK_TYPE_CHOICES,
        default=LINK_INTERNAL,
    )
    placement = models.CharField(
        '位置',
        max_length=10,
        choices=PLACEMENT_CHOICES,
        default=PLACEMENT_HEADER,
    )
    order = models.PositiveSmallIntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)
    open_in_new_tab = models.BooleanField('新标签页打开', default=False)

    class Meta:
        ordering = ['placement', 'order', 'id']
        verbose_name = '导航 / 页脚链接'
        verbose_name_plural = '导航与页脚链接'

    def __str__(self):
        return f'{self.label}（{self.get_placement_display()}）'

    def href(self):
        if self.link_type == self.LINK_EXTERNAL:
            return self.url
        return self.url


class SiteProfile(models.Model):
    site_name = models.CharField('站点名称', max_length=100, default='MyBlog')
    tagline = models.CharField('站点标语', max_length=200, blank=True)
    about_sidebar = models.TextField(
        '侧栏简介',
        blank=True,
        default='写代码是热爱，写到世界充满爱！',
        help_text='侧栏「关于博主」简介',
    )
    about_page_html = models.TextField(
        '关于页内容',
        blank=True,
        help_text='关于页正文（支持 HTML，模板中安全渲染）',
    )
    resume_title = models.CharField(
        '简历页标题',
        max_length=100,
        blank=True,
        default='',
        help_text='留空则前台显示「个人简历」',
    )
    resume_tagline = models.CharField(
        '简历页副标题',
        max_length=200,
        blank=True,
        help_text='显示在横幅说明文字；留空可使用站点标语',
    )
    resume_markdown = models.TextField(
        '简历页内容',
        blank=True,
        help_text='Markdown 格式；前台渲染规则与文章正文一致（见 settings 中 MARKDOWNX_* 扩展）',
    )
    author_display_name = models.CharField('博主显示名', max_length=80, blank=True, default='博客作者')
    github_url = models.URLField('GitHub', blank=True)
    twitter_url = models.URLField('Twitter', blank=True)
    bilibili_url = models.URLField('哔哩哔哩', blank=True)
    email = models.EmailField('联系邮箱', blank=True)
    icp_number = models.CharField(
        'ICP 备案号',
        max_length=80,
        blank=True,
        help_text='显示在页脚，例：京ICP备12345678号；无需展示可留空',
    )
    icp_url = models.URLField(
        '备案信息链接',
        blank=True,
        help_text='可选，指向工信部备案查询页或主办单位公示页，备案号将可点击打开',
    )

    class Meta:
        verbose_name = '站点信息'
        verbose_name_plural = '站点信息'

    def __str__(self):
        return self.site_name
