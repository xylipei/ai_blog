# MySQL: utf8 -> utf8mb4，避免 emoji / 部分生僻字写入失败 (OperationalError 1366)

from django.db import migrations


def convert_blog_tables_utf8mb4(apps, schema_editor):
    if schema_editor.connection.vendor != 'mysql':
        return
    # 与 utf8mb4_unicode_ci 兼容常见 MySQL 5.7/8.0
    sql = "CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    tables = [
        'blog_post',
        'blog_category',
        'blog_tag',
        'blog_comment',
        'blog_navlink',
        'blog_siteprofile',
        'blog_post_tags',
    ]
    with schema_editor.connection.cursor() as cursor:
        for table in tables:
            cursor.execute(f"ALTER TABLE `{table}` {sql}")


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_content_help_markdownx'),
    ]

    operations = [
        migrations.RunPython(convert_blog_tables_utf8mb4, noop_reverse),
    ]
