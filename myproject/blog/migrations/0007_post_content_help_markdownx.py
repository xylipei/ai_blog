from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_content_help_easymde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(
                help_text='使用 Markdown 编写；后台使用 django-markdownx 编辑器，可实时预览。',
                verbose_name='正文',
            ),
        ),
    ]
