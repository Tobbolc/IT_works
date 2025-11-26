from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01.forms import (BuyerLoginForm, SellerLoginForm, BuyerRegisterForm,
                         SellerRegisterForm, ForgetpwdForm, ChangepwdForm,
                         BuyerInfoForm, BuyerRechargeForm, AddCommodityForm, DetailForm)
from app01.models import Commodity, Buyer, Seller, Order, Comment
from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination


def index(request):
    """首页 角色0"""
    if request.session.get('info_buyer', ''):
        return redirect('index_buyer')
    elif request.session.get('info_seller', ''):
        return redirect('index_seller')
    else:
        data_search = {}
        search = request.GET.get('q', "")
        if search:
            data_search["name__contains"] = search

        queryset = Commodity.objects.filter(**data_search, putaway_state=2).order_by("-clicks")  # 按照用户点击量倒序获取

        page_object = Pagination(request, queryset)

        content = {
            'queryset': page_object.page_queryset,
            'page_string': page_object.html(),
            'search': search
        }
        return render(request, 'index.html', content)


def register_buyer(request):
    """买家注册"""
    if request.method == 'GET':
        form = BuyerRegisterForm()
        return render(request, 'register_buyer.html', {'form': form})
    else:
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password']
            password2 = md5(form.cleaned_data['password2'])
            if Buyer.objects.filter(username=username).exists():
                form.add_error('username', '用户名已存在')
            elif Buyer.objects.filter(phone=phone).exists():
                form.add_error('phone', '该手机号码已被注册')
            elif password1 != password2:
                form.add_error('password2', '两次密码不一致')
            else:
                form.save()
                return redirect('login_buyer')
        return render(request, 'register_buyer.html', {'form': form})


def register_seller(request):
    """卖家注册"""
    if request.method == 'GET':
        form = SellerRegisterForm()
        return render(request, 'register_seller.html', {'form': form})
    else:
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            store_name = form.cleaned_data['store_name']
            phone = form.cleaned_data['phone']
            password1 = form.cleaned_data['password']
            password2 = md5(form.cleaned_data['password2'])
            if Seller.objects.filter(store_name=store_name).exists():
                form.add_error('store_name', '店铺名称已存在')
            elif Seller.objects.filter(phone=phone).exists():
                form.add_error('phone', '该手机号码已被注册')
            elif password1 != password2:
                form.add_error('password2', '两次密码不一致')
            else:
                form.save()
                return redirect('/')
        return render(request, 'register_seller.html', {'form': form})


from app01.utils.code import check_code
from io import BytesIO


def image_code(request):
    """生成图片验证码"""
    img, code_string = check_code()

    # 写入session中
    request.session['image_code'] = code_string
    # session设置60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, format='PNG')
    return HttpResponse(stream.getvalue())


def login_buyer(request):
    """买家登录（账号密码）"""
    if request.method == 'GET':
        form = BuyerLoginForm()
        return render(request, 'login_buyer.html', {'form': form})
    else:
        username = request.POST.get('username')
        request.session['forgetpwd_buyer'] = username
        form = BuyerLoginForm(data=request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']

            # 验证码的校验
            user_input_code = form.cleaned_data.pop('code')  # pop 不将user_input_code作为过滤条件去数据库里查找，防止出错
            code = request.session.get('image_code', "")
            if code.upper() != user_input_code.upper():
                form.add_error("code", "图片验证码错误")
                return render(request, 'login_buyer.html', {'form': form})

            user_object = Buyer.objects.filter(**form.cleaned_data).first()
            # 错误
            if not user_object:
                form.add_error("password", "用户名或密码错误")
                return render(request, 'login_buyer.html', {'form': form})
            # 正确
            # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中
            request.session['info_buyer'] = {'id': user_object.id, 'username': user_object.username,
                                             'account': user_object.account}
            # 7天免登录
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('index_buyer')
        return render(request, 'login_buyer.html', {'form': form})


def login_seller(request):
    if request.method == 'GET':
        form = SellerLoginForm()
        return render(request, 'login_seller.html', {'form': form})
    else:
        store_name = request.POST.get('store_name')
        request.session['forgetpwd_seller'] = store_name  # 写入session传参
        form = SellerLoginForm(data=request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']

            # 验证码的校验
            user_input_code = form.cleaned_data.pop('code')  # pop 不将user_input_code作为过滤条件去数据库里查找，防止出错
            code = request.session.get('image_code', "")
            if code.upper() != user_input_code.upper():
                form.add_error("code", "图片验证码错误")
                return render(request, 'login_seller.html', {'form': form})

            user_object = Seller.objects.filter(**form.cleaned_data).first()
            # 错误
            if not user_object:
                form.add_error("password", "店铺名称或密码错误")
                return render(request, 'login_seller.html', {'form': form})
            # 正确
            # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中
            request.session['info_seller'] = {'id': user_object.id, 'store_name': user_object.store_name}
            # 7天免登录
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('index_seller')
        return render(request, 'login_seller.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/')


def index_buyer(request):
    data_search = {}
    search = request.GET.get('q', "")
    if search:
        data_search["name__contains"] = search
    queryset = Commodity.objects.filter(**data_search, putaway_state=2).order_by("-clicks")  # 按照用户点击量倒序获取
    content = {
        'queryset': queryset,
    }
    return render(request, "index_buyer.html", content)


def index_seller(request):
    store_name = request.session["info_seller"]['store_name']
    store = Seller.objects.filter(store_name=store_name).first()
    products = Commodity.objects.filter(store_id=store.id).all()
    orders = Order.objects.filter(seller=store_name).all()
    form = AddCommodityForm
    content = {
        'shop': store,
        'products': products,
        'orders': orders,
        'form': form
    }
    return render(request, 'index_seller.html', content)


from app01.utils.code import generate_random_code
from django.core.mail import send_mail
from DjangoProject_mall import settings


# def email_code(request):
#     """发邮件"""
#     code = generate_random_code()
#
#     # 写入session
#     request.session['email_code'] = code
#     # session设置60秒超时
#     request.session.set_expiry(60)
#     subject = '登录验证邮件'
#     message = code
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [request.POST['email']]
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=from_email,
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )


def forget_pwd(request):
    """忘记密码"""
    username = request.session.get('forgetpwd_buyer', '')
    store_name = request.session.get('forgetpwd_seller', '')
    if username:
        form = ForgetpwdForm()
        user = Buyer.objects.filter(username=username).first()
        if not user:
            return HttpResponse('您输入了错误的用户名!请重试')
        content = {
            'form': form, 'username': username, 'email': user.email, 'store_name': store_name
        }
        if request.method == 'GET':
            # print(username)
            # #清除session中的用户名，避免重复使用
            # if 'forgetpwd' in request.session:
            #     del request.session['forgetpwd']
            if request.session.get('email_sent', False):  # False是默认值，当‘email_sent’不存在时返回False 防止重复发邮件
                return render(request, 'forget_pwd.html', content)
            else:
                """发邮件"""
                code = generate_random_code()
                # 写入session
                request.session['email_code'] = code
                # session设置60秒超时
                request.session.set_expiry(60)
                subject = '登录验证邮件'
                message = code, "此邮件一分钟内有效"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                request.session['email_sent'] = True  # 利用session标记已发送邮件，避免重复发送
            return render(request, 'forget_pwd.html', content)
        elif request.method == 'POST':
            form = ForgetpwdForm(data=request.POST)
            if form.is_valid():
                # 先校验验证码
                user_input_email_code = form.cleaned_data.pop('code')  # pop
                code = request.session.get('email_code', "")
                if code.upper() != user_input_email_code.upper():
                    form.add_error("code", "邮箱验证码错误")
                    return render(request, 'forget_pwd.html', content)

                # 正确 跳转到修改密码页面
                return redirect('change_pwd')
        return render(request, 'forget_pwd.html', content)
    elif store_name:
        form = ForgetpwdForm()
        user = Seller.objects.filter(store_name=store_name).first()
        if not user:
            return HttpResponse('您输入了错误的店铺名!请重试')
        content = {
            'form': form, 'username': username, 'email': user.email, 'store_name': store_name
        }
        if request.method == 'GET':
            # print(username)
            # #清除session中的用户名，避免重复使用
            # if 'forgetpwd' in request.session:
            #     del request.session['forgetpwd']
            if request.session.get('email_sent', False):  # False是默认值，当‘email_sent’不存在时返回False 防止重复发邮件
                return render(request, 'forget_pwd.html', content)
            else:
                """发邮件"""
                code = generate_random_code()
                # 写入session
                request.session['email_code'] = code
                # session设置60秒超时
                request.session.set_expiry(60)
                subject = '登录验证邮件'
                message = code, "此邮件一分钟内有效"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                request.session['email_sent'] = True  # 利用session标记已发送邮件，避免重复发送
            return render(request, 'forget_pwd.html', content)

        elif request.method == 'POST':
            form = ForgetpwdForm(data=request.POST)
            if form.is_valid():
                # 先校验验证码
                user_input_email_code = form.cleaned_data.pop('code')  # pop
                code = request.session.get('email_code', "")
                if code.upper() != user_input_email_code.upper():
                    form.add_error("code", "邮箱验证码错误")
                    return render(request, 'forget_pwd.html', content)

                # 正确 跳转到修改密码页面
                return redirect('change_pwd')
        return render(request, 'forget_pwd.html', content)


import os
from django.core.files.base import ContentFile


def selfpage_buyer(request):
    """买家个人主页"""
    user_get = request.session.get('info_buyer')['username']
    user = Buyer.objects.filter(username=user_get).first()
    form = BuyerInfoForm
    form1 = BuyerRechargeForm
    if request.method == 'GET':
        return render(request, 'selfpage_buyer.html', {'user': user, 'form': form, "form1": form1})
    # print(request.FILES)
    file_object = request.FILES.get("avatar")

    # 指定保存路径
    file_path = os.path.join('media/avatar', file_object.name)

    # 使用open函数保存文件
    with open(file_path, "wb+") as destination:
        for chunk in file_object.chunks():
            destination.write(chunk)
        destination.close()

    user.avatar.save(file_object.name, ContentFile(open(file_path, 'rb').read()), save=True)
    return render(request, 'selfpage_buyer.html', {'user': user, 'form': form, "form1": form1})


# <MultiValueDict: {'avatar': [<InMemoryUploadedFile: 84e1deb5cca53881a57449ca88734d4e.png (image/png)>]}>


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def changeinfo_buyer(request):
    """买家修改个人信息(Ajax请求)"""
    username_old = request.session.get('info_buyer')['username']
    form = BuyerInfoForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        Buyer.objects.filter(username=username_old).update(username=username, email=email, phone=phone)
        return JsonResponse({"status": True})
    #       return HttpResponse(json.dumps({"status": True}))
    return JsonResponse({"status": False, 'error': form.errors})


@csrf_exempt
def add_commodity(request):
    """卖家发布新商品（create）(ajax)"""
    store = request.session['info_seller']['store_name']
    store_id = Seller.objects.filter(store_name=store).first().label
    last_commodity = Commodity.objects.order_by('id').last()  # 获取最后一条商品数据
    form = AddCommodityForm(data=request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        price = form.cleaned_data['price']
        price_b = form.cleaned_data['price_b']
        stock = form.cleaned_data['stock']
        Commodity.objects.create(name=name, photo="photo/artknife.jpg", price=price, price_b=price_b,
                                 stock=stock, store_id=store_id, clicks=last_commodity.clicks + 1, putaway_state=1,
                                 cart_state=1, label=store_id)
        return JsonResponse({"status": True})
        #       return HttpResponse(json.dumps({"status": True}))
    return JsonResponse({"status": False, 'error': form.errors})


@csrf_exempt
def accountadd_buyer(request):
    """买家充钱"""
    account_old = request.session.get('info_buyer')['account']
    username = request.session.get('info_buyer')['username']
    form = BuyerRechargeForm(data=request.POST)
    if form.is_valid():
        account_add = form.cleaned_data['account']  # 要充多少钱
        account_new = account_old + float(account_add)
        Buyer.objects.filter(username=username, account=account_old).update(account=account_new)
    return JsonResponse({"status": True})


def commodity_detail(request, nid):
    if request.method == 'GET':
        commodity = Commodity.objects.filter(id=nid).first()
        comment_list = Comment.objects.filter(commodity_id=nid).all()
        content = {
            'datum': commodity,
            'comment_list': comment_list
        }
        return render(request, 'commodity_detail.html', content)


from app01.utils.order_id import generate_oid


def commodity_order(request, nid):
    """订单详情页"""
    """创建订单号"""
    oid = generate_oid()
    now = datetime.now()
    flag = 0  # 默认是未提交状态 即未创建订单
    orderlist = Order.objects.filter(commodity_id=nid).first()
    if orderlist:
        if orderlist.process_state == 1:  # 处理中
            flag = 1
        elif orderlist.process_state == 2:  # 已拒绝
            flag = 2
        else:  # 已通过
            flag = 3
    commodity = Commodity.objects.filter(id=nid).all()
    content = {
        'commodity': commodity,
        'order_id': oid,
        'now': now,
        'flag': flag
    }
    return render(request, 'order_detail.html', content)


def change_pwd(request):
    username_get = request.session.get('forgetpwd_buyer', '')
    store_name_get = request.session.get('forgetpwd_seller', '')
    if username_get:
        if request.method == 'GET':
            form = ChangepwdForm
            return render(request, 'changepwd.html', {'form': form})
        else:
            form = ChangepwdForm(data=request.POST)
            if form.is_valid():
                password_o = form.cleaned_data['password_old']
                password_n = form.cleaned_data['password_new']
                user_object = Buyer.objects.filter(password=md5(password_o)).first()
                # 错误
                if not user_object:
                    form.add_error("password_old", "旧密码错误或用户不存在")
                    return render(request, 'changepwd.html', {'form': form})
                # 正确
                Buyer.objects.filter(password=md5(password_o), username=username_get).update(password=md5(password_n))
                return redirect('selfpage_buyer')
            return render(request, 'changepwd.html', {'form': form})
    elif store_name_get:
        if request.method == 'GET':
            form = ChangepwdForm
            return render(request, 'changepwd.html', {'form': form})
        else:
            form = ChangepwdForm(data=request.POST)
            if form.is_valid():
                password_o = form.cleaned_data['password_old']
                password_n = form.cleaned_data['password_new']
                user_object = Buyer.objects.filter(password=md5(password_o)).first()
                # 错误
                if not user_object:
                    form.add_error("password_old", "旧密码错误或店铺不存在")
                    return render(request, 'changepwd.html', {'form': form})
                # 正确
                Seller.objects.filter(password=md5(password_o), store_name=store_name_get).update(
                    password=md5(password_n))
                return redirect('index_seller')
            return render(request, 'changepwd.html', {'form': form})


@csrf_exempt  # 在实际应用中，建议使用其他方法处理CSRF，而不是禁用
def add_cart(request):
    product_id = request.POST.get('product_id')
    # 在这里处理商品ID，查询数据库 更新购物车
    # print(product_id)
    Commodity.objects.filter(id=product_id).update(cart_state=2)  # 变为已加入购物车
    return JsonResponse({'status': 'success', 'product_id': product_id})


def index_cart(request):
    user_get = request.session.get("info_buyer")['username']
    commodity = Commodity.objects.filter(cart_state=2).all()
    count = Commodity.objects.filter(cart_state=2).count()
    content = {
        'user_get': user_get,
        'commodity': commodity,
        'count': count
    }
    return render(request, 'index_cart.html', content)


def order_history(request):
    user_get = request.session.get("info_buyer")['username']
    orders = Order.objects.filter(buyer=user_get).all()
    count = Order.objects.filter(buyer=user_get).count()
    commodity_ids = orders.values_list('commodity_id', flat=True)
    commodity = Commodity.objects.filter(id__in=commodity_ids)
    # commodity = Commodity.objects.filter(id=order.commodity_id).all()
    content = {
        'user_get': user_get,
        'commodity': commodity,
        'count': count
    }
    return render(request, 'order_history.html', content)


@csrf_exempt
def order_deal_buyer(request):
    quantity = request.POST.get('quantity')
    product_id = request.POST.get('product_id')
    tap = request.POST.get('tap')
    # 校验余额
    user_get = request.session.get('info_buyer')['username']  # 获取买家名称
    buyer = Buyer.objects.filter(username=user_get).first()
    account_buyer = buyer.account  # 买家钱包里的钱
    stock_product = Commodity.objects.filter(id=product_id).first().stock  # 商品库存
    commodity = Commodity.objects.filter(id=product_id).first()

    total = float(commodity.price) * float(quantity)  # 商品总价
    if int(tap) == 1:  # 创建订单
        if account_buyer >= total:  # 成功 创建订单
            if buyer.is_active == 1:  # 买家账户是激活状态
                oid = generate_oid()
                now = datetime.now()
                account_buyer -= total  # 卖家处理完订单后要更新买家的钱
                stock_product -= int(quantity)  # 更新库存
                Order.objects.create(oid=oid, commodity_id=product_id, title=commodity.name, price=total
                                     , quantity=quantity, process_state=1, buyer=user_get, seller=commodity.store,
                                     created_at=now)
                Buyer.objects.filter(username=user_get).update(account=account_buyer)
                Commodity.objects.filter(id=product_id).update(stock=stock_product)
                return JsonResponse({'status': True})
        else:  # 钱不够
            return JsonResponse({"status": False})
    else:  # 取消订单
        account_buyer += total
        stock_product += int(quantity)
        Order.objects.filter(commodity_id=product_id).delete()
        Buyer.objects.filter(username=user_get).update(account=account_buyer)  # 退款
        Commodity.objects.filter(id=product_id).update(stock=stock_product)  # 返还数量
        return JsonResponse({"status": True})


@csrf_exempt
def order_deal_seller(request, order_id):
    """卖家处理订单页（展示与订单详情页类似）"""
    store_name = request.session['info_seller']['store_name']
    seller = Seller.objects.filter(store_name=store_name).first()
    order = Order.objects.filter(id=order_id).first()
    state = order.process_state
    commodity = Commodity.objects.filter(id=order.commodity_id).first()
    if request.method == 'GET':
        content = {
            'order': order,
            'state': state,
            'commodity': commodity
        }
        return render(request, 'order_deal_seller.html', content)
    else:
        quantity = request.POST.get('quantity')
        tap = request.POST.get('tap')
        if int(tap) == 1:  # 同意该订单
            if seller.is_active == 1:
                Order.objects.filter(id=order.id).update(process_state=3)
                return JsonResponse({"status": True})
        else:  # 拒绝该订单 要退款和返回库存
            if seller.is_active == 1: # 卖家必须是激活状态
                stock = commodity.stock
                account = Buyer.objects.filter(username=order.buyer).first().account
                total = float(commodity.price) * float(quantity)  # 商品总价
                account += total
                stock += int(quantity)
                Commodity.objects.filter(id=order.commodity_id).update(stock=stock)  # 返还库存
                Buyer.objects.filter(username=order.buyer).update(account=account)  # 退款
                Order.objects.filter(id=order.id).update(process_state=2)
                return JsonResponse({'status': True})


def storeinfo_buyer(request, store_id):
    shop = Seller.objects.filter(id=store_id).first()
    products = Commodity.objects.filter(label=store_id).all()
    return render(request, 'store_info_buyer.html', {"products": products, "shop": shop})


def commodity_manage(request, nid):
    request.session['nid'] = nid
    datum = Commodity.objects.filter(id=nid).first()
    form_detail = DetailForm
    form = AddCommodityForm
    comment_list = Comment.objects.filter(commodity_id=nid, seller_id=None).all()
    if request.method == 'GET':
        content = {
            'datum': datum,
            'form_detail': form_detail,
            "form": form,
            'comment_list': comment_list
        }
        return render(request, 'commodity_manage.html', content)
    else:
        form_detail = DetailForm(data=request.POST)
        if form_detail.is_valid():
            detail = form_detail.cleaned_data['detail']
            Commodity.objects.filter(id=nid).update(detail=detail)
        content = {
            'datum': datum,
            'form_detail': form_detail,
            'form': form,
            'comment_list': comment_list
        }
        return render(request, 'commodity_manage.html', content)


@csrf_exempt
def commodity_manage_seller(request):
    """卖家上下架或删除商品"""
    store = request.session['info_seller']['store_name']
    seller = Seller.objects.filter(store_name=store).first()
    commodity_id = request.POST.get('Id')
    tap = request.POST.get('tap')
    if int(tap) == 0:  # 上架
        if seller.is_active == 1:
            Commodity.objects.filter(id=commodity_id).update(putaway_state=2)
            return JsonResponse({"status": True})
    elif int(tap) == 1:  # 下架
        if seller.is_active == 1:
            Commodity.objects.filter(id=commodity_id).update(putaway_state=1)
            return JsonResponse({"status": True})
    else:  # 删除
        if seller.is_active == 1:
            Commodity.objects.filter(id=commodity_id).delete()
            return JsonResponse({"status": True})


@csrf_exempt
def changeinfo_commodity(request):
    """卖家修改商品信息(Ajax请求)"""
    id = request.session.get('nid','')
    form = AddCommodityForm(data=request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        price = form.cleaned_data['price']
        price_b = form.cleaned_data['price_b']
        stock = form.cleaned_data['stock']
        Commodity.objects.filter(id=id).update(name=name, price=price, price_b=price_b, stock=stock)
        return JsonResponse({"status": True})
    #       return HttpResponse(json.dumps({"status": True}))
    return JsonResponse({"status": False, 'error': form.errors})
@csrf_exempt
def comment_manage(request):
    if 'info_buyer' in request.session:
        buyer_name = request.session['info_buyer']['username']
        buyer = Buyer.objects.filter(username=buyer_name).first()
        content = request.POST.get('comment_content')
        commodity_id = request.POST.get('commodity_id')
        pid = request.POST.get('pid')
        Comment.objects.create(content=content, commodity_id=commodity_id, parent_id=pid, buyer_id=buyer.id)
        return JsonResponse({"status": True})
    elif 'info_seller' in request.session:
        store_name = request.session['info_seller']['store_name']
        seller = Seller.objects.filter(store_name=store_name).first()
        content = request.POST.get('comment_content')
        commodity_id = request.POST.get('commodity_id')
        pid = request.POST.get('pid')
        Comment.objects.create(content=content, commodity_id=commodity_id, parent_id=pid, seller_id=seller.id)
        return JsonResponse({"status": True})

def comment_delete(request, cid):
    Comment.objects.filter(id=cid).delete()
    return HttpResponse("删除成功！")