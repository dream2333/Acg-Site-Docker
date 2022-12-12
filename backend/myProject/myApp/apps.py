from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myApp'
    
class UsersConfig(AppConfig):
    name = 'myApp'
    verbose_name = "数据管理"     #新添加一行