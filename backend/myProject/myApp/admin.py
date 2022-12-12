from django.contrib import admin

from .models import Video, Message, Article, User
from django.contrib.auth.admin import UserAdmin

admin.site.site_title = "浏览器标签页"
admin.site.site_header = "管理界面header"
admin.site.index_title = "主页"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message", "user", "timestamp", "link_to")
    list_per_page = 18


@admin.register(Article)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "_text", "timestamp")
    list_per_page = 18

    def _text(self, obj):
        if len(obj.text) > 20:
            return obj.text[0:30] + "..."
        else:
            return obj.text

    _text.short_description = "预览"


@admin.register(User)
class UserInfoAdmin(UserAdmin):
    list_display = ("username", "email", "is_superuser", "last_login")
    list_per_page = 18
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "个人信息",
            {"fields": ("avatar", "signature", "email", "mobile", "tags")},
        ),
        (
            "账号权限",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups"),
            },
        ),
        (
            "其他信息",
            {"fields": ("last_login", "date_joined","liked")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_filter = (
        "is_superuser",
        "is_active",
    )
    search_fields = ("username", "email")
    ordering = ("username",)
    filter_horizontal = ()


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_per_page = 18


