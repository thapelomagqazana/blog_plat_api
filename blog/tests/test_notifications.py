from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Notification, NotificationPreference

CustomUser = get_user_model()

class NotificationTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.client.login(username='testuser', password='testpassword')
        self.notification = Notification.objects.create(
            user=self.user,
            message='This is a test notification.'
        )
        self.notification_preference = NotificationPreference.objects.create(
            user=self.user,
            email_notifications=True,
            push_notifications=True
        )
        self.notification_list_url = reverse('notification-list')
        self.mark_notification_read_url = reverse('mark-notification-read', kwargs={'pk': self.notification.pk})
        self.notification_preferences_url = reverse('notification-preferences')

    def test_list_notifications(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.notification_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'This is a test notification.')

    def test_mark_notification_as_read(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.mark_notification_read_url, {'is_read': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_retrieve_notification_preferences(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.notification_preferences_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['email_notifications'])
        self.assertTrue(response.data['push_notifications'])

    def test_update_notification_preferences(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.notification_preferences_url, {'email_notifications': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification_preference.refresh_from_db()
        self.assertFalse(self.notification_preference.email_notifications)