from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import BlogPost, Like

CustomUser = get_user_model()

class LikeTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )
        self.like_url = reverse('like-post', kwargs={'pk': self.blog_post.pk})
        self.unlike_url = reverse('unlike-post', kwargs={'pk': self.blog_post.pk})

    def test_like_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.blog_post.likes.count(), 1)

    def test_unlike_post(self):
        Like.objects.create(user=self.user, post=self.blog_post)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.unlike_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(self.blog_post.likes.count(), 0)

    def test_prevent_duplicate_likes(self):
        Like.objects.create(user=self.user, post=self.blog_post)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.blog_post.likes.count(), 1)