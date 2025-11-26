from datetime import datetime
from decimal import Decimal

from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Commodity(models.Model):
    name = models.CharField(max_length=100, verbose_name="商品名称")
    photo = models.ImageField(blank=True, null=True, upload_to="photo/")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品现价",
                                validators=[MinValueValidator(Decimal('0.01'))])
    price_b = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品原价",
                                  validators=[MinValueValidator(Decimal('0.01'))], default=1000.00)
    stock = models.IntegerField(default=0, verbose_name="商品库存")
    clicks = models.IntegerField(default=0, verbose_name="用户点击量")
    label_choices = (
        (1, '居家生活'), (2, '数码科技'), (3, '潮流轻奢'),
        (4, '时尚穿搭'), (5, '美妆个护'), (6, '食品生鲜'),
        (7, '运动户外'), (8, '图书文创')
    )
    label = models.SmallIntegerField(verbose_name='标签', choices=label_choices, default=1)
    putaway_choices = (
        (1, '下架'),
        (2, '上架')
    )
    putaway_state = models.SmallIntegerField(verbose_name='上架状态', choices=putaway_choices, default=1)
    cart_choices = (
        (1, '未添加'),
        (2, '已添加')
    )
    cart_state = models.SmallIntegerField(verbose_name='加入购物车', choices=cart_choices, default=1)
    store = models.ForeignKey(verbose_name="店家", to='Seller', to_field='id', on_delete=models.CASCADE, default=1)
    detail = RichTextField(verbose_name='商品详情', config_name='default',
                           default='这是一条商品详情内容')  # config_name指定ckeditor配置文件，不指定就使用default

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Seller(models.Model):
    store_name = models.CharField(verbose_name="店铺名称", max_length=32, unique=True)
    seller_name = models.CharField(verbose_name="负责人姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    phone = models.CharField(verbose_name="手机号码", max_length=11, unique=True)
    email = models.EmailField(blank=True, null=True)
    label_choices = (
        (1, '居家生活'), (2, '数码科技'), (3, '潮流轻奢'),
        (4, '时尚穿搭'), (5, '美妆个护'), (6, '食品生鲜'),
        (7, '运动户外'), (8, '图书文创')
    )
    label = models.SmallIntegerField(verbose_name='标签', choices=label_choices, default=1)
    is_actice_choices = (
        (1, '激活'),
        (2, '冻结')
    )
    is_active = models.SmallIntegerField(verbose_name="账户状态", choices=is_actice_choices, default=1)

    class Meta:
        verbose_name = '卖家'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.store_name


class Buyer(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    phone = models.CharField(verbose_name="手机号码", max_length=11, unique=True)
    email = models.EmailField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar/")
    # account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="账户余额", default=30000.00, validators=[MinValueValidator(Decimal('0.01'))])
    account = models.FloatField(verbose_name="账户余额")
    is_active_choices = (
        (1, '激活'),
        (2, '冻结')
    )
    is_active = models.SmallIntegerField(verbose_name="账户状态", choices=is_active_choices, default=1)

    class Meta:
        verbose_name = '买家'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.account = round(self.account, 2)
        super(Buyer, self).save(*args, **kwargs)


class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=64, default="202502110104")
    commodity_id = models.IntegerField(verbose_name='商品id', default=1)
    # commodity = models.ForeignKey(verbose_name='商品', to='Commodity', to_field='id', on_delete=models.CASCADE, default=1)
    title = models.CharField(verbose_name="名称", max_length=32, default="电动牙刷")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总价",
                                validators=[MinValueValidator(Decimal('0.01'))])
    quantity = models.IntegerField(verbose_name="数量", default=1)
    process_choices = (
        (1, '未处理'),
        (2, '已拒绝'),
        (3, '已通过'),
    )
    process_state = models.SmallIntegerField(verbose_name='订单处理状态', choices=process_choices, default=1)
    buyer = models.CharField(verbose_name="买家", max_length=32, default='Tobbolc')
    seller = models.CharField(verbose_name="卖家", max_length=32, default='生活王')
    created_at = models.DateTimeField(verbose_name='时间', default=datetime.now)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    commodity = models.ForeignKey(to="Commodity", to_field='id',on_delete=models.CASCADE, related_name='comments')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(verbose_name="评论内容")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
