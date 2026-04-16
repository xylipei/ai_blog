from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Category, Comment, NavLink, Post, Tag


class BlogSmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('author1', 'a1@example.com', 'pass')
        cls.category = Category.objects.create(name='DemoCat')
        p = Post.objects.create(
            title='Hello World',
            slug='hello-world',
            author=cls.user,
            content='正文内容用于测试。',
            excerpt='摘要',
            category=cls.category,
            status='published',
        )
        tg = Tag.objects.create(name='TagOne', slug='tag-one')
        p.tags.add(tg)

    def test_home_ok(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_post_detail_ok(self):
        r = self.client.get('/post/hello-world/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Hello World')

    def test_about_ok(self):
        r = self.client.get('/about/')
        self.assertEqual(r.status_code, 200)

    def test_archive_ok(self):
        r = self.client.get('/archive/')
        self.assertEqual(r.status_code, 200)

    def test_archive_month_ok(self):
        p = Post.objects.get(slug='hello-world')
        r = self.client.get(f'/archive/{p.created_on.year}/{p.created_on.month}/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Hello World')

    def test_category_list_ok(self):
        r = self.client.get('/categories/')
        self.assertEqual(r.status_code, 200)

    def test_search_pagination_ok(self):
        r = self.client.get('/search/', {'q': 'Hello'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Hello World')

    def test_rss_feed_ok(self):
        r = self.client.get('/feed/rss/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('application/rss+xml', r['Content-Type'])
        self.assertContains(r, 'Hello World')

    def test_nav_links_seeded(self):
        self.assertTrue(NavLink.objects.filter(placement=NavLink.PLACEMENT_HEADER).exists())

    def test_tag_page_ok(self):
        r = self.client.get('/tag/tag-one/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Hello World')


class CommentModerationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('cuser', 'c@example.com', 'pass')
        cls.category = Category.objects.create(name='C')
        cls.post = Post.objects.create(
            title='P',
            slug='p-slug',
            author=cls.user,
            content='x',
            category=cls.category,
            status='published',
        )

    def test_new_comment_not_active(self):
        c = Client()
        r = c.post(
            '/post/p-slug/',
            {
                'name': 'Visitor',
                'email': 'v@example.com',
                'body': 'Needs moderation',
            },
        )
        self.assertEqual(r.status_code, 302)

        cm = Comment.objects.get(post=self.post, email='v@example.com')
        self.assertFalse(cm.active)
