# 模型 verbose_name 汉化（仅元数据，不改变数据库列语义）

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_nav_tag_site_and_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '分类', 'verbose_name_plural': '分类'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name'], 'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={
                'ordering': ['-created_on'],
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_on'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
        migrations.AlterModelOptions(
            name='navlink',
            options={
                'ordering': ['placement', 'order', 'id'],
                'verbose_name': '导航 / 页脚链接',
                'verbose_name_plural': '导航与页脚链接',
            },
        ),
        migrations.AlterModelOptions(
            name='siteprofile',
            options={'verbose_name': '站点信息', 'verbose_name_plural': '站点信息'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=60, unique=True, verbose_name='URL 别名'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='URL 别名'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='blog_posts',
                to=settings.AUTH_USER_MODEL,
                verbose_name='作者',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='特色图片'),
        ),
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.TextField(blank=True, null=True, verbose_name='摘要'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='posts',
                to='blog.category',
                verbose_name='分类',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(
                blank=True,
                related_name='posts',
                to='blog.tag',
                verbose_name='标签',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(
                choices=[('draft', '草稿'), ('published', '已发布')],
                default='draft',
                max_length=10,
                verbose_name='状态',
            ),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='blog.post',
                verbose_name='文章',
            ),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=80, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='电子邮箱'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='提交时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False, verbose_name='已通过审核'),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='label',
            field=models.CharField(max_length=100, verbose_name='显示文字'),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='url',
            field=models.CharField(
                help_text='站内填写路径，如 /about/；外链写完整地址 https://…',
                max_length=500,
                verbose_name='链接地址',
            ),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='link_type',
            field=models.CharField(
                choices=[('internal', '站内路径'), ('external', '外部链接')],
                default='internal',
                max_length=10,
                verbose_name='链接类型',
            ),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='placement',
            field=models.CharField(
                choices=[('header', '顶部导航'), ('footer', '页脚链接')],
                default='header',
                max_length=10,
                verbose_name='位置',
            ),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='排序'),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='启用'),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='open_in_new_tab',
            field=models.BooleanField(default=False, verbose_name='新标签页打开'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='site_name',
            field=models.CharField(default='MyBlog', max_length=100, verbose_name='站点名称'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='tagline',
            field=models.CharField(blank=True, max_length=200, verbose_name='站点标语'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='about_sidebar',
            field=models.TextField(
                blank=True,
                default='写代码是热爱，写到世界充满爱！',
                help_text='侧栏「关于博主」简介',
                verbose_name='侧栏简介',
            ),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='about_page_html',
            field=models.TextField(
                blank=True,
                help_text='关于页正文（支持 HTML，模板中安全渲染）',
                verbose_name='关于页内容',
            ),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='author_display_name',
            field=models.CharField(blank=True, default='博客作者', max_length=80, verbose_name='博主显示名'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='github_url',
            field=models.URLField(blank=True, verbose_name='GitHub'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='twitter_url',
            field=models.URLField(blank=True, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='bilibili_url',
            field=models.URLField(blank=True, verbose_name='哔哩哔哩'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='联系邮箱'),
        ),
    ]
