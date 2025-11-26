"""
URL configuration for DjangoProject_mall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from app01 import views

urlpatterns = [
          path('', views.index, name='index'), # 角色0的全局首页 未登录
          path('index/buyer/', views.index_buyer, name='index_buyer'), # 买家首页 index_buyer.html
          path('index/seller/', views.index_seller, name='index_seller'), # 卖家主页 index_seller.html
          path('register/buyer/', views.register_buyer, name='register_buyer'), # 买家注册 register_buyer.html
          path('login/buyer/', views.login_buyer, name='login_buyer'), # 买家登录 login_buyer.html
          path('logout/', views.logout, name='logout'), # 卖家与买家的登出
          path('image/code/', views.image_code), # 图片验证码
          path('register/seller/', views.register_seller, name='register_seller'), # 卖家注册 register_seller.html
          path('login/seller/', views.login_seller, name='login_seller'), # 卖家登录 login_seller.html
          # path('email/code/', views.email_code),
          path('forget/pwd/', views.forget_pwd, name='forget_pwd'), # 卖家买家忘记密码 forget_pwd.html
          path('change/pwd/', views.change_pwd, name='change_pwd'), # 卖家买家修改新密码 changepwd.html
          path('selfpage/buyer/', views.selfpage_buyer, name='selfpage_buyer'), # 买家主页（个人中心） selfpage_buyer.html
          path('changeinfo/buyer/', views.changeinfo_buyer, name='changeinfo_buyer'), # 买家修改个人信息（ajax）
          path('commodity/<int:nid>/detail/', views.commodity_detail, name='commodity_detail'), # 买家视角的商品详情页 commodity_detail.html
          path('commodity/<int:nid>/order/', views.commodity_order, name='commodity_order'), # 买家视角的订单详情页 order_detail.html
          path('add/cart/', views.add_cart, name='add_cart'), # 买家在商品详情页添加购物车（ajax）
          path('index/cart/', views.index_cart, name='index_cart'), # 买家的购物车展示页面 index_cart.html
          path('order/history/', views.order_history, name='order_history'), #买家的历史订单 order_history.html
          path('accountadd/buyer/', views.accountadd_buyer, name='accountadd_buyer'), # 买家的钱包充值（ajax）
          path('order/deal/', views.order_deal_buyer, name='order_deal_buyer'), # 买家提交订单 取消订单 （ajax）
          path('add/commodity/', views.add_commodity, name='add_commodity'), # 卖家发布新品（ajax）
          path('order/<int:order_id>/deal/', views.order_deal_seller, name='order_deal_seller'), # 卖家处理订单 包含展示详情和处理（ajax） order_deal_seller.html
          path('store/<int:store_id>/buyer/', views.storeinfo_buyer, name='storeinfo_buyer'), # 买家视角的店铺详情页 store_info_buyer.html
          path('commodity/<int:nid>/manage/', views.commodity_manage, name='commodity_manage'), # 卖家的商品管理页
          path('commodity/manage/', views.commodity_manage_seller, name='commodity_manage_seller'), # 卖家上下架商品或删除商品（ajax）
          path('change/commodityinfo/', views.changeinfo_commodity, name='changeinfo_commodity'), # 卖家上下架商品或删除商品（ajax）
          path('comment/manage/', views.comment_manage, name='comment_manage'), # 卖家上下架商品或删除商品（ajax）
          path('comment/<int:cid>/delete/', views.comment_delete, name='comment_delete'), # 卖家上下架商品或删除商品（ajax）

]
urlpatterns += [
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)