from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import BlogPost, Comment, Like, PostView

CustomUser = get_user_model()

class AnalyticsTests(APITestCase):

    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(username='admin', password='adminpassword', email='admin@example.com')
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.client.login(username='admin', password='adminpassword')
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.blog_post,
            content='This is a test comment.',
            author=self.user
        )
        Like.objects.create(user=self.user, post=self.blog_post)
        PostView.objects.create(user=self.user, post=self.blog_post)
        self.analytics_url = reverse('analytics')

    def test_analytics(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.analytics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['active_users'], 2)
        self.assertEqual(response.data['total_posts'], 1)
        self.assertEqual(response.data['total_comments'], 1)
        self.assertEqual(response.data['total_likes'], 1)
        self.assertEqual(response.data['total_views'], 1)