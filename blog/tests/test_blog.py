from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import BlogPost

CustomUser = get_user_model()

class BlogPostTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.blog_post_data = {
            'title': 'Test Blog Post',
            'content': 'This is a test blog post.',
            'author': self.user
        }
        self.blog_post = BlogPost.objects.create(**self.blog_post_data)
        self.list_create_url = reverse('post-list-create')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.blog_post.pk})

    def test_create_blog_post(self):
        new_blog_post_data = {
            'title': 'New Blog Post',
            'content': 'This is a new blog post.',
            'author': self.user.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_create_url, new_blog_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 2)
        self.assertEqual(BlogPost.objects.get(id=response.data['id']).title, 'New Blog Post')

    def test_retrieve_blog_post(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.blog_post.title)

    def test_update_blog_post(self):
        updated_blog_post_data = {
            'title': 'Updated Blog Post',
            'content': 'This is an updated blog post.',
            'author': self.user.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url, updated_blog_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updated Blog Post')

    def test_delete_blog_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), 0)

    def test_pagination(self):
        # Create additional blog posts to test pagination
        for i in range(15):
            BlogPost.objects.create(title=f'Blog Post {i}', content='Content', author=self.user)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Assuming page_size is 10

    def test_caching(self):
        # Retrieve the blog post to cache it
        self.client.force_authenticate(user=self.user)
        self.client.get(self.detail_url)
        # Update the blog post
        updated_blog_post_data = {
            'title': 'Updated Blog Post',
            'content': 'This is an updated blog post.',
            'author': self.user.id
        }
        self.client.put(self.detail_url, updated_blog_post_data, format='json')
        # Retrieve the blog post again to check if cache is updated
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Blog Post')