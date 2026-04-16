from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_siteprofile_icp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(
                help_text='使用 Markdown 编写；后台编辑时可实时预览。',
                verbose_name='正文',
            ),
        ),
    ]
