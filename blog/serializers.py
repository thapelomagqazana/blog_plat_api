from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import (BlogPost, Comment, Like,
                      PostView, Notification, NotificationPreference)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model, used to serialize/deserialize user data.
    
    Meta:
        model (User): The user model being serialized.
        fields (tuple): The fields to include in the serialized output.
        extra_kwargs (dict): Additional keyword arguments for fields. The password field is write-only.
        
    Methods:
        create(validated_data): Creates a new user instance with the given validated data.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates and returns a new user with encrypted password.
        
        Args:
            validated_data (dict): Validated data for the user.
            
        Returns:
            User: The created user instance.
        """
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login data.
    
    Attributes:
        username (CharField): The username of the user.
        password (CharField): The user's password.
    """
    username = serializers.CharField()
    password = serializers.CharField()

class TOTPDeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for the TOTPDevice model, used for two-factor authentication.
    
    Meta:
        model (TOTPDevice): The TOTP device model being serialized.
        fields (tuple): The fields to include in the serialized output.
    """
    class Meta:
        model = TOTPDevice
        fields = ('id', 'name', 'confirmed')

class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the BlogPost model, used to serialize/deserialize blog post data.

    Attributes:
        like_count (SerializerMethodField): A field to get the count of likes for the blog post.
    
    Meta:
        model (BlogPost): The blog post model being serialized.
        fields (str): Specifies that all fields in the model should be included.
    """
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_view_count(self, obj):
        return PostView.objects.filter(post=obj).count()

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model, including nested replies.
    
    Attributes:
        replies (SerializerMethodField): A custom field to retrieve nested replies for a comment.
        
    Meta:
        model (Comment): The model being serialized.
        fields (str): Specifies that all fields in the Comment model should be included.
        
    Methods:
        get_replies(obj): Retrieves serialized data for any replies associated with the comment.
    """
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return None

class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    
    Meta:
        model (Like): The model being serialized.
        fields (str): Specifies that all fields in the Like model should be included.
    """
    class Meta:
        model = Like
        fields = '__all__'

class PostViewSerializer(serializers.ModelSerializer):
    """
    Serializer for the PostView model.
    
    Meta:
        model (PostView): The model being serialized.
        fields (str): Specifies that all fields in the PostView model should be included.
    """
    class Meta:
        model = PostView
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.

    Meta:
        model (Notification): The model being serialized.
        fields (str): Specifies that all fields in the Notification model should be included.
    """
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for the NotificationPreference model.

    Meta:
        model (NotificationPreference): The model being serialized.
        fields (str): Specifies that all fields in the NotificationPreference model should be included.
    """
    class Meta:
        model = NotificationPreference
        fields = '__all__'

