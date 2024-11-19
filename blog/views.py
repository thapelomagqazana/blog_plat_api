from rest_framework import generics, status, views
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from .serializers import UserSerializer, LoginSerializer, TOTPDeviceSerializer
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.cache import cache
from .models import BlogPost
from .serializers import BlogPostSerializer

class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(ResetPasswordRequestToken):
    permission_classes = [AllowAny]

class PasswordResetConfirmView(ResetPasswordConfirm):
    permission_classes = [AllowAny]

class TOTPDeviceView(generics.ListCreateAPIView):
    queryset = TOTPDevice.objects.all()
    serializer_class = TOTPDeviceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlogPostPagination(PageNumberPagination):
    page_size = 10

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BlogPostPagination

    def get_queryset(self):
        queryset = cache.get('blog_posts')
        if not queryset:
            queryset = BlogPost.objects.all()
            cache.set('blog_posts', queryset, timeout=60*15)  # Cache for 15 minutes
        return queryset

class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj = cache.get(f'blog_post_{self.kwargs["pk"]}')
        if not obj:
            obj = super().get_object()
            cache.set(f'blog_post_{self.kwargs["pk"]}', obj, timeout=60*15)  # Cache for 15 minutes
        return obj

    def perform_update(self, serializer):
        instance = serializer.save()
        cache.set(f'blog_post_{instance.pk}', instance, timeout=60*15)
        cache.delete('blog_posts')

    def perform_destroy(self, instance):
        cache.delete(f'blog_post_{instance.pk}')
        cache.delete('blog_posts')
        instance.delete()