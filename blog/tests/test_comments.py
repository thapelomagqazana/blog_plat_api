from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import BlogPost, Comment

CustomUser = get_user_model()

class CommentTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )
        self.comment_data = {
            'post': self.blog_post.id,
            'content': 'This is a test comment.',
            'author': self.user.id
        }
        self.comment = Comment.objects.create(
            post=self.blog_post,
            content='This is a test comment.',
            author=self.user
        )
        self.list_create_url = reverse('comment-list-create')
        self.detail_url = reverse('comment-detail', kwargs={'pk': self.comment.pk})

    def test_create_comment(self):
        new_comment_data = {
            'post': self.blog_post.id,
            'content': 'This is a new comment.',
            'author': self.user.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_create_url, new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.get(id=response.data['id']).content, 'This is a new comment.')

    def test_retrieve_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.comment.content)

    def test_update_comment(self):
        updated_comment_data = {
            'post': self.blog_post.id,
            'content': 'This is an updated comment.',
            'author': self.user.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url, updated_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'This is an updated comment.')

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_create_nested_comment(self):
        nested_comment_data = {
            'post': self.blog_post.id,
            'content': 'This is a nested comment.',
            'author': self.user.id,
            'parent': self.comment.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_create_url, nested_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.get(id=response.data['id']).content, 'This is a nested comment.')
        self.assertEqual(Comment.objects.get(id=response.data['id']).parent.id, self.comment.id)

    def test_retrieve_nested_comments(self):
        nested_comment = Comment.objects.create(
            post=self.blog_post,
            content='This is a nested comment.',
            author=self.user,
            parent=self.comment
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['replies']), 1)
        self.assertEqual(response.data['replies'][0]['content'], nested_comment.content)