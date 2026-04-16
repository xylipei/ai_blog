# 将简历正文字段重命名为 resume_markdown，保留原有数据（勿用 Remove+Add）

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_resume_navlink'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteprofile',
            old_name='resume_html',
            new_name='resume_markdown',
        ),
    ]
