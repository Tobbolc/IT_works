from datetime import  datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

class User(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=32,unique=True)
    password = models.CharField(verbose_name="密码",max_length=64)
    email = models.EmailField(blank=True,null=True)
    avatar = models.ImageField(blank=True,null=True,upload_to="avatar/")
    def __str__(self):
        return self.username

class BlindBoxData(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=100)
    age = models.IntegerField(verbose_name='年龄')
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    email = models.EmailField(verbose_name='邮箱', max_length=100)
    contact = models.CharField(verbose_name='联系方式',max_length=100)
    address = models.CharField(verbose_name='住址',max_length=100)
    introduction = models.CharField(verbose_name='个人简介',max_length=500,blank=True,null=True)
    demand = models.CharField(verbose_name='需求',max_length=500,blank=True,null=True)
    user = models.ForeignKey(verbose_name='用户',to="User",to_field="username",on_delete=models.CASCADE,default='Tobbolc')
    created_at = models.DateTimeField(verbose_name='时间',default=datetime.now)
    def __str__(self):
        return self.name

class Comment(models.Model):
    content = RichTextUploadingField(config_name='default',)
    created_at = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(verbose_name='用户',to="User",to_field="username",on_delete=models.CASCADE,default='Tobbolc')
    # blind_box = models.ForeignKey(verbose_name='评论',to="BlindBoxData",to_field="id",on_delete=models.CASCADE,default=1,unique=True)
    # def __str__(self):
    #     return f'{self.user.username} on {self.created_at}'

class ChosenMyself(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=100)
    age = models.IntegerField(verbose_name='年龄')
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, default=1)
    email = models.EmailField(verbose_name='邮箱', max_length=100)
    contact = models.CharField(verbose_name='联系方式', max_length=100)
    address = models.CharField(verbose_name='住址', max_length=100)
    introduction = models.CharField(verbose_name='个人简介', max_length=500, blank=True, null=True)
    demand = models.CharField(verbose_name='需求', max_length=500, blank=True, null=True)
    user = models.ForeignKey(verbose_name='用户', to="User", to_field="username", on_delete=models.CASCADE, default='Tobbolc')
    created_at = models.DateTimeField(verbose_name='时间', default=datetime.now)

class BlindboxComment(models.Model):
    content = models.CharField(verbose_name='评论内容', max_length=500)
    created_at = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    user = models.ForeignKey(verbose_name='用户', to="User", to_field="username", on_delete=models.CASCADE, default='Tobbolc')
    blind_box = models.ForeignKey(verbose_name='评论', to="BlindBoxData", to_field="id", on_delete=models.CASCADE,default=3)


