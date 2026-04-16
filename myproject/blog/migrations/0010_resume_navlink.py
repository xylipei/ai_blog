# 为已有站点补充「简历」导航（若尚不存在）

from django.db import migrations


def add_resume_navlink(apps, schema_editor):
    NavLink = apps.get_model('blog', 'NavLink')
    if NavLink.objects.filter(url='/resume/').exists():
        return
    NavLink.objects.create(
        label='简历',
        url='/resume/',
        link_type='internal',
        placement='header',
        order=4,
        is_active=True,
        open_in_new_tab=False,
    )


def noop_reverse(apps, schema_editor):
    NavLink = apps.get_model('blog', 'NavLink')
    NavLink.objects.filter(url='/resume/', label='简历').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_siteprofile_resume'),
    ]

    operations = [
        migrations.RunPython(add_resume_navlink, noop_reverse),
    ]
