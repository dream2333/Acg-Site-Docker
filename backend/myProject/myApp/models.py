
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField, CharField, DateField
from django.core.validators import MaxValueValidator, MinValueValidator

class Video(models.Model):
    title = models.CharField("名称", max_length=150, default="")
    intro = models.CharField("简介", max_length=200, default="")
    timestamp = models.DateTimeField("时间", auto_now_add=True)
    cover = models.ImageField(
        verbose_name="封面",
        upload_to="img/",
        null=True,
        blank=True,
        help_text=("封面长宽比必须为1.6:1,否则可能产生显示错误"),
    )
    video = models.FileField("视频", upload_to="video/", default="video/test_video.mp4")
    tags = models.CharField(
        "视频标签", help_text=("请用空格分隔"), max_length=200, default="日漫 搞笑", blank=True
    )

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = "视频"
        
    def __str__(self) -> str:
        return self.title

class User(AbstractUser):
    signature = models.CharField(max_length=30, blank=True, verbose_name="签名档")
    mobile = models.CharField(
        max_length=11,
        verbose_name="手机号",
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name="头像", upload_to="img/", default="img/defaultAvatar.png"
    )
    is_staff = models.BooleanField(
        "管理权限",
        default=False,
        help_text=("用户是否可以登录到后台管理页面"),
    )
    is_active = models.BooleanField(
        "登录权限", default=True, help_text="账户是否可用，禁用此选项可在不删除账号的前提下封禁用户."
    )
    is_superuser = models.BooleanField(
        "超级管理员",
        default=False,
        help_text=("用户是否具有全部的用户组权限，勾选后无需添加组权限"),
    )
    first_name = None
    last_name = None
    tags = models.CharField(
        "个人标签", help_text=("请用空格分隔"), max_length=200, default="新用户 文艺青年", blank=True
    )

    liked = models.ManyToManyField(Video,verbose_name="喜欢的视频",blank=True)

    def __str__(self) -> str:
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    cover = models.ImageField(
        verbose_name="封面",
        upload_to="img/",
        null=True,
        blank=True,
        help_text=("封面长宽比必须为1.6:1,否则可能产生显示错误"),
    )
    text = models.TextField(verbose_name="内容")
    timestamp = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="作者", null=True, blank=True
    )

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def __str__(self) -> str:
        return self.title


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="用户")
    message = models.CharField(max_length=100, verbose_name="留言")
    timestamp = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    link_to = models.ForeignKey(
        to=Video,
        on_delete=models.CASCADE,
        verbose_name="关联到",
        null=True,
        blank=True,
    )
    rating =  models.FloatField("评分",validators=[MaxValueValidator(5), MinValueValidator(0)],null=True,blank=True)
    def __str__(self) -> str:
        return self.message

    class Meta:
        verbose_name = "留言"
        verbose_name_plural = "留言"