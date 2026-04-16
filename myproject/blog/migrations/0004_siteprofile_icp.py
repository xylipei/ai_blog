from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_model_verbose_name_zh'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='icp_number',
            field=models.CharField(
                blank=True,
                help_text='显示在页脚，例：京ICP备12345678号；无需展示可留空',
                max_length=80,
                verbose_name='ICP 备案号',
            ),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='icp_url',
            field=models.URLField(
                blank=True,
                help_text='可选，指向工信部备案查询页或主办单位公示页，备案号将可点击打开',
                verbose_name='备案信息链接',
            ),
        ),
    ]
