from django.urls import path
from .views import (RegisterView, LoginView, LogoutView, 
                    PasswordResetView, PasswordResetConfirmView, 
                    TOTPDeviceView, BlogPostListCreateView, 
                    BlogPostRetrieveUpdateDestroyView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('totp/', TOTPDeviceView.as_view(), name='totp'),
    path('posts/', BlogPostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', BlogPostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
]