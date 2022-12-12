"""myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from myApp import views
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # path(r"", RedirectView.as_view(url="http://127.0.0.1:3000")),
    path(r"", RedirectView.as_view(url="admin/")),
    path(r"admin/", admin.site.urls),
    path(r"API/user/register/", views.UserViewSet.as_view({"post": "register"})),
    path(r"API/user/login/", views.UserViewSet.as_view({"post": "login"})),
    path(r"API/user/logout/", views.UserInfoViewSet.as_view({"get": "logout"})),
    path(
        r"API/user/info/",
        views.UserInfoViewSet.as_view({"get": "get", "post": "update"}),
    ),
    path(
        r"API/video/like/<int:video_id>/",
        views.UserInfoViewSet.as_view({"get": "like_video"}),
    ),
    path(r"API/message/list/", views.MessageListViewSet.as_view({"get": "get"})),
    path(
        r"API/video/<int:link_to>/comment/",
        views.MessageListViewSet.as_view({"get": "get_comment"}),
    ),
    path(r"API/video/comment/", views.CommentViewSet.as_view()),
    path(r"API/article/list/", views.ArticleListViewSet.as_view()),
    path(r"API/article/<int:pk>/", views.ArticleDetailViewSet.as_view()),
    path(r"API/video/list/", views.VideoListViewSet.as_view()),
    path(r"API/video/<int:pk>/", views.VideoInfoViewSet.as_view()),
    path(r"API/video/search/", views.VideoSearchViewSet.as_view()),
    path(
        r"API/video/like/list/",
        views.UserInfoViewSet.as_view({"get": "get_liked"}),
    ),
    path(
        r"API/video/like/remove/<int:video_id>/",
        views.UserInfoViewSet.as_view({"get": "remove_liked"}),
    ),
    path(r"API/message/my/", views.MyMessageViewSet.as_view()),
    #path(r"API/test", views.Test.as_view()), #测试代码api 不要使用
    path(r"API/homemenu",views.HomeMenuInfoViewSet.as_view()),
    # path(r"media/video/<str:path>",views.stream_video),
    # path(r"API/recommend/init",views.RecommendViewSet.as_view({"get":"init"})),
    # path(r"API/recommend/calc",views.RecommendViewSet.as_view({"get":"calc_user_sim"})),
    # path(r"API/recommend/<str:user_id>",views.RecommendViewSet.as_view({"get":"recommend"})),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
