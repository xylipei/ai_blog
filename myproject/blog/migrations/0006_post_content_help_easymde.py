from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_content_markdown_help'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(
                help_text='使用 Markdown 编写；后台使用 EasyMDE 编辑器，可预览与分栏预览。',
                verbose_name='正文',
            ),
        ),
    ]
