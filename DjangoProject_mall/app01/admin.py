from django.contrib import admin
from django.contrib import messages
from app01 import models

# Register your models here.


admin.site.register(models.Buyer)
admin.site.register(models.Seller)


class LabelFilter(admin.SimpleListFilter):
    title = '商品标签'
    parameter_name = 'label'

    def lookups(self, request, model_admin):
        return models.Commodity.label_choices  # 直接使用你定义好的 choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(label=self.value())


@admin.register(models.Commodity)
class CommodityAdmin(admin.ModelAdmin):
    # 过滤配置
    list_filter = [
        LabelFilter,  # 按商品标签过滤（显示选项：居家生活、数码科技等） 直接显示标签内容
        'putaway_state',  # 按上架状态过滤（额外补充）
    ]

    # 搜索配置（按名称和标签搜索）
    search_fields = [
        'name',
    ]
    # 添加自定义批量操作
    actions = ['batch_putaway', 'batch_remove']

    # 批量上架操作
    def batch_putaway(self, request, queryset):
        updated = queryset.update(putaway_state=2)  # 直接更新数据库，无需遍历对象
        self.message_user(request, f"成功上架 {updated} 个商品", messages.SUCCESS)

    batch_putaway.short_description = "▶ 批量上架选中的商品"  # 显示在操作下拉框中的名称

    # 批量下架操作
    def batch_remove(self, request, queryset):
        updated = queryset.update(putaway_state=1)
        self.message_user(request, f"成功下架 {updated} 个商品", messages.SUCCESS)

    batch_remove.short_description = "◀ 批量下架选中的商品"


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    # 过滤配置
    list_filter = [
        'created_at',  # 按订单创建时间过滤（自动生成日期分层过滤）
        'process_state'  # 按订单处理状态过滤
    ]

    # 搜索配置（按订单号、商品名称、买家/卖家名称搜索）
    search_fields = [
        'oid',  # 订单号
        'title',  # 商品标题
        'buyer',  # 买家名称
        'seller'  # 卖家名称
    ]
