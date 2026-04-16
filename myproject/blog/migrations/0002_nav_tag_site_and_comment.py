# Generated manually for NavLink, Tag, SiteProfile, Post.tags, Comment.default

from django.db import migrations, models


def seed_nav_and_site(apps, schema_editor):
    NavLink = apps.get_model('blog', 'NavLink')
    SiteProfile = apps.get_model('blog', 'SiteProfile')
    if not NavLink.objects.exists():
        NavLink.objects.bulk_create(
            [
                NavLink(
                    label='首页',
                    url='/',
                    link_type='internal',
                    placement='header',
                    order=0,
                    is_active=True,
                    open_in_new_tab=False,
                ),
                NavLink(
                    label='文章分类',
                    url='/categories/',
                    link_type='internal',
                    placement='header',
                    order=1,
                    is_active=True,
                    open_in_new_tab=False,
                ),
                NavLink(
                    label='归档',
                    url='/archive/',
                    link_type='internal',
                    placement='header',
                    order=2,
                    is_active=True,
                    open_in_new_tab=False,
                ),
                NavLink(
                    label='关于',
                    url='/about/',
                    link_type='internal',
                    placement='header',
                    order=3,
                    is_active=True,
                    open_in_new_tab=False,
                ),
                NavLink(
                    label='Django 官网',
                    url='https://www.djangoproject.com/',
                    link_type='external',
                    placement='footer',
                    order=0,
                    is_active=True,
                    open_in_new_tab=True,
                ),
            ]
        )
    if not SiteProfile.objects.exists():
        SiteProfile.objects.create(
            site_name='MyBlog',
            tagline='写代码是热爱，写到世界充满爱！',
            about_sidebar='写代码是热爱，写到世界充满爱！',
            about_page_html='<p>这是个人博客站点，记录学习、工作与生活。可在后台「站点信息」中修改本页内容。</p>',
            author_display_name='博客作者',
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=60, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='NavLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('url', models.CharField(help_text='站内填写路径，如 /about/；外链写完整地址 https://…', max_length=500)),
                ('link_type', models.CharField(choices=[('internal', '站内路径'), ('external', '外部链接')], default='internal', max_length=10)),
                ('placement', models.CharField(choices=[('header', '顶部导航'), ('footer', '页脚链接')], default='header', max_length=10)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('open_in_new_tab', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '导航 / 页脚链接',
                'verbose_name_plural': '导航与页脚链接',
                'ordering': ['placement', 'order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='MyBlog', max_length=100)),
                ('tagline', models.CharField(blank=True, max_length=200)),
                ('about_sidebar', models.TextField(blank=True, default='写代码是热爱，写到世界充满爱！', help_text='侧栏「关于博主」简介')),
                ('about_page_html', models.TextField(blank=True, help_text='关于页正文（支持 HTML，模板中安全渲染）')),
                ('author_display_name', models.CharField(blank=True, default='博客作者', max_length=80)),
                ('github_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('bilibili_url', models.URLField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
            options={
                'verbose_name': '站点信息',
                'verbose_name_plural': '站点信息',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog.tag'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(seed_nav_and_site, noop_reverse),
    ]
