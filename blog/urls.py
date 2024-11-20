from django.urls import path
from .views import (RegisterView, LoginView, LogoutView, 
                    PasswordResetView, PasswordResetConfirmView, 
                    TOTPDeviceView, BlogPostListCreateView, 
                    BlogPostRetrieveUpdateDestroyView,
                    CommentListCreateView, CommentRetrieveUpdateDestroyView,
                    LikePostView, UnlikePostView, AnalyticsView,
                    NotificationListView, MarkNotificationAsReadView, 
                    NotificationPreferenceView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('totp/', TOTPDeviceView.as_view(), name='totp'),
    path('posts/', BlogPostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', BlogPostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('notification-preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
]