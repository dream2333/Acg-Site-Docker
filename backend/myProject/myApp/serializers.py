from rest_framework import serializers
from .models import Article, Video, User, Message


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        avatar = serializers.ImageField()
        fields = ("username", "avatar", "last_login")


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        avatar = serializers.ImageField()

        fields = (
            "username",
            "signature",
            "avatar",
            "mobile",
            "is_superuser",
            "email",
            "date_joined",
            "last_login",
            "tags",
            "liked"
        )


class MessageSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            avatar = serializers.ImageField()
            fields = (
                "username",
                "avatar",
            )

    user = UserSerializer()

    class Meta:
        model = Message
        fields = (
            "message",
            "timestamp",
            "user",
            "rating",
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"

    def get_username(self, obj):
        if obj.user != None:
            return obj.user.username
        else:
            return "无作者"


# 视频详细信息
class VideoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


# 视频列表页
class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "title",
            "cover",
            "timestamp",
        )


# 文章列表页
class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ("id", "title", "cover", "timestamp","username")

    def get_username(self, obj):
        if obj.user != None:
            return obj.user.username
        else:
            return "无作者"
