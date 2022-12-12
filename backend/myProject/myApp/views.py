from io import BytesIO
from wsgiref.util import FileWrapper
from django.conf import settings
from rest_framework.decorators import api_view
import json
import mimetypes
import os
from random import shuffle
import re
from .recommendUtils.User import UserBasedCF
from django.http import StreamingHttpResponse
from rest_framework.authtoken.models import Token
from django.contrib import auth
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from .serializers import (
    VideoListSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    VideoInfoSerializer,
    MessageSerializer,
    UserInfoSerializer,
    UserLoginSerializer,
)

from .models import Article, Video, Message, User

class PagerPagination(PageNumberPagination):
    max_page_size = 18  # 每页最大数目
    page_size = 18


def round_away_from_zero(a):
    return int((a * 10 + 5) // 10)


# 无需验证的登陆注册
class UserViewSet(ViewSet):
    authentication_classes = ()
    permission_classes = ()

    def register(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            User.objects.create_user(username=username, password=password)
            return Response({"status": 1, "msg": "注册成功"})
        except Exception as e:
            return Response({"status": 0, "msg": "查询出错", "error": str(e)})

    def login(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                # 添加用户token
                auth.login(request, user_obj)
                oid_token = Token.objects.filter(user=user_obj)
                oid_token.delete()
                token = Token.objects.create(user=user_obj)
                return Response(
                    {
                        "status": 1,
                        "msg": UserLoginSerializer(
                            auth.get_user(request), context={"request": request}
                        ).data,
                        "token": token.key,
                    }
                )
            else:
                return Response({"status": 0, "msg": "验证失败"})
        except Exception as e:
            return Response({"status": 0, "msg": "查询出错", "error": str(e)})


# 需要验证的用户api
class UserInfoViewSet(ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = auth.get_user(request)
        return Response(UserInfoSerializer(user, context={"request": request}).data)

    def update(self, request):
        try:
            user = auth.get_user(request)
            # 反序列化
            serializer = UserInfoSerializer(user, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": 1, "msg": "更新成功"})
        except Exception as e:
            return Response({"status": 0, "msg": "更新失败", "error": str(e)})

    def like_video(self, request, video_id):
        try:
            user = auth.get_user(request)
            # 反序列化
            video = Video.objects.get(id=video_id)
            user.liked.add(video)
            return Response({"status": 1, "msg": "更新成功"})
        except Exception as e:
            return Response({"status": 0, "msg": "更新失败", "error": str(e)})

    def get_liked(self, request):
        try:
            user = auth.get_user(request)
            # 反序列化
            queryset = user.liked.all()
            serializer = VideoListSerializer(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as e:
            return Response({"status": 0, "msg": "更新失败", "error": str(e)})

    def remove_liked(self, request, video_id):
        try:
            user = auth.get_user(request)
            # 反序列化
            video = Video.objects.get(id=video_id)
            user.liked.remove(video)
            return Response({"status": 1, "msg": "更新成功"})
        except Exception as e:
            return Response({"status": 0, "msg": "更新失败", "error": str(e)})

    def logout(self, request):
        # 从token中删除用户
        request.auth.delete()
        return Response({"status": 1, "msg": "登出成功"})


# 读取留言板列表
class MessageListViewSet(ViewSet):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        queryset = Message.objects.filter(link_to_id=None)
        data = MessageSerializer(queryset, many=True, context={"request": request}).data
        return Response(data)

    def get_comment(self, request, link_to):
        queryset = Message.objects.filter(link_to_id=link_to)
        data = MessageSerializer(queryset, many=True, context={"request": request}).data
        return Response(data)


# 读取文章的粗略列表
class ArticleListViewSet(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filter_backends = [OrderingFilter]


# 读取某个文章内容
class ArticleDetailViewSet(RetrieveAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer


# 读取视频的评论信息
class VideoCommentViewSet(RetrieveAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Video.objects.all()
    serializer_class = VideoInfoSerializer


# 读取某个视频详情信息
class VideoInfoViewSet(RetrieveAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Video.objects.all()
    serializer_class = VideoInfoSerializer


# 读取所有视频详情信息
class VideoListViewSet(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer
    pagination_class = PageNumberPagination  # 配置分页类
    filter_backends = [OrderingFilter]


# 读取首页菜单
class HomeMenuInfoViewSet(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        try:
            ac = Article.objects.count()
            vc = Video.objects.count()
            lc = auth.get_user(request).liked.count()
            return Response({"article": ac, "video": vc, "liked": lc})
        except:
            return Response({"article": ac, "video": vc, "liked": 0})


# 视频搜索
class VideoSearchViewSet(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ""
    serializer_class = VideoListSerializer
    pagination_class = PagerPagination  # 配置分页类

    def list(self, request, *args, **kwargs):
        query = Video.objects.filter(title__contains=request.query_params["query"])
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return super().get_queryset()


# 我的留言
class MyMessageViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = auth.get_user(request)
        queryset = Message.objects.filter(user=user, link_to_id=None).all()
        return Response(MessageSerializer(queryset, many=True).data)

    def post(self, request):
        try:
            user = auth.get_user(request)
            Message(user=user, message=request.data["text"]).save()
            return Response({"status": 1, "msg": "留言成功"})
        except:
            return Response(
                {
                    "status": 0,
                    "msg": "查询出错",
                }
            )


class CommentViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = auth.get_user(request)
            m = Message.objects.filter(
                ~Q(rating=None), user=user.id, link_to_id=request.data["link_to_id"]
            )
            print(len(m))
            if len(m) == 0:
                Message(
                    user=user,
                    message=request.data["text"],
                    link_to_id=request.data["link_to_id"],
                    rating=request.data["rating"],
                ).save()
                return Response({"status": 1, "msg": "留言成功"})
            else:
                if request.data["rating"] == None:
                    Message(
                        user=user,
                        message=request.data["text"],
                        link_to_id=request.data["link_to_id"],
                    ).save()
                    return Response({"status": 2, "msg": "留言成功"})
                else:
                    return Response({"status": 0, "msg": "您已经评过分了"})
        except Exception as e:
            return Response(
                {
                    "status": 0,
                    "msg": "查询出错" + str(e),
                }
            )

# # 将视频文件以流媒体的方式响应，测试环境可用
# @api_view(["GET"])
# def stream_video(request, path):
#     def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
#         with open(file_name, "rb") as f:
#             f.seek(offset, os.SEEK_SET)
#             remaining = length
#             while True:
#                 bytes_length = (
#                     chunk_size if remaining is None else min(remaining, chunk_size)
#                 )
#                 data = f.read(bytes_length)
#                 if not data:
#                     break
#                 if remaining:
#                     remaining -= len(data)
#                 yield data
#     path = settings.MEDIA_ROOT + "video/" + path
#     range_header = request.META.get("HTTP_RANGE", "").strip()
#     range_re = re.compile(r"bytes\s*=\s*(\d+)\s*-\s*(\d*)", re.I)
#     range_match = range_re.match(range_header)
#     size = os.path.getsize(path)
#     content_type, encoding = mimetypes.guess_type(path)
#     content_type = content_type or "application/octet-stream"
#     if range_match:
#         first_byte, last_byte = range_match.groups()
#         first_byte = int(first_byte) if first_byte else 0
#         last_byte = first_byte + 1024 * 1024 * 8  # 8M 每片,响应体最大体积
#         if last_byte >= size:
#             last_byte = size - 1
#         length = last_byte - first_byte + 1
#         resp = StreamingHttpResponse(
#             file_iterator(path, offset=first_byte, length=length),
#             status=206,
#             content_type=content_type,
#         )
#         resp["Content-Length"] = str(length)
#         resp["Content-Range"] = "bytes %s-%s/%s" % (first_byte, last_byte, size)
#     else:
#         # 不是以视频流方式的获取时，以生成器方式返回整个文件，节省内存
#         resp = StreamingHttpResponse(
#             FileWrapper(open(path, "rb")), content_type=content_type
#         )
#         resp["Content-Length"] = str(size)
#     resp["Accept-Ranges"] = "bytes"
#     return resp
