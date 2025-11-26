from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from DjangoProject_blindbox import settings
from app01.models import BlindBoxData, User, ChosenMyself, BlindboxComment
from app01.utils.bootstrap import BootstrapForm, BootstrapModelform
from .forms import CommentForm


def blindbox_index(request):
    return render(request, 'index.html')


class BlindBoxDataForm(forms.ModelForm):
    introduction = forms.CharField(max_length=500, label='个人简介')
    demand = forms.CharField(max_length=500, label='需求')

    class Meta:
        model = BlindBoxData
        fields = ['name', 'age', 'gender', 'email', 'contact', 'address', 'introduction', 'demand', 'created_at']
        # widgets = {
        #     'name':forms.TextInput(attrs={'class':'form-control'}),
        #     'age':forms.NumberInput(attrs={'class':'form-control'}),
        #     'gender':forms.Select(attrs={'class':'form-control'}),
        #     'email':forms.EmailInput(attrs={'class':'form-control'}),
        #     'contact':forms.TextInput(attrs={'class':'form-control'}),
        #     'address':forms.TextInput(attrs={'class':'form-control'}),
        #     'introduction':forms.Textarea(attrs={'class':'form-control'}),
        #     'demand':forms.Textarea(attrs={'class':'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": 'form-control', "placeholder": field.label}


def blindbox_add(request):
    """添加盲盒"""
    if request.method == 'GET':
        form = BlindBoxDataForm()
        return render(request, 'blindbox_add.html', {'form': form})
    form = BlindBoxDataForm(data=request.POST)
    if form.is_valid():
        form.save()

        user_now = request.session['info']['username']
        latest_id = BlindBoxData.objects.order_by('-id').values('id').first()['id']
        BlindBoxData.objects.filter(id=latest_id).update(user=user_now)
        # 水平受限 —————— 由于要从session中获取username赋给blindbox的外键user，故不可以直接将user_id设成与id关联的数据，而应设成与username关联的

        gender = form.cleaned_data['gender']
        if gender == 1:
            return redirect('blindbox_male')
        elif gender == 2:
            return redirect('blindbox_female')
    return render(request, 'blindbox_add.html', {'form': form})


from django.utils.safestring import mark_safe


def blindbox_list_male(request):
    """男生盲盒"""
    page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size
    datalist = BlindBoxData.objects.filter(gender=1)[start:end]
    # 数据总条数
    total_count = BlindBoxData.objects.filter(gender=1).count()
    # 总页数
    page_count, div = divmod(total_count, page_size)
    if div:
        page_count += 1
    # 显示前5页和后5页
    plus = 5
    if page_count <= 2 * plus + 1:
        # 页数比较少，未达到11页
        start_page = 1
        end_page = page_count
    else:
        # 页数比较多

        # 当前页<5时
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > page_count:
                start_page = page_count - 2 * plus
                end_page = page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 页码列表
    page_str_list = []
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 下一页
    if page < page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page_count)
    page_str_list.append(prev)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(page_count))

    data_male = BlindBoxData.objects.filter(gender=1).count()
    data_user = User.objects.all().count()

    search_string = """
       <li>
           <form style="float: left;margin-left: -1px" method="get">
               <div class="input-group" style="width: 200px">
                   <input type="text" name="page" class="form-control" placeholder="页码" 
                          style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                   <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
               </div>
           </form>
       </li>
       """
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {
        'data1': data_male,
        'data2': data_user,
        'datalist': datalist,
        'page_string': page_string,
    }
    return render(request, 'blindbox_list_male.html', context)


def blindbox_list_female(request):
    """女生盲盒"""
    page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size
    datalist = BlindBoxData.objects.filter(gender=2)[start:end]
    # 数据总条数
    total_count = BlindBoxData.objects.filter(gender=2).count()
    # 总页数
    page_count, div = divmod(total_count, page_size)
    if div:
        page_count += 1
    # 显示前5页和后5页
    plus = 5
    if page_count <= 2 * plus + 1:
        # 页数比较少，未达到11页
        start_page = 1
        end_page = page_count
    else:
        # 页数比较多

        # 当前页<5时
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > page_count:
                start_page = page_count - 2 * plus
                end_page = page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 页码列表
    page_str_list = []
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 下一页
    if page < page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page_count)
    page_str_list.append(prev)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(page_count))

    data_female = BlindBoxData.objects.filter(gender=2).count()
    data_user = User.objects.all().count()

    search_string = """
           <li>
               <form style="float: left;margin-left: -1px" method="get">
                   <div class="input-group" style="width: 200px">
                       <input type="text" name="page" class="form-control" placeholder="页码" 
                              style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                       <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                   </div>
               </form>
           </li>
           """
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))

    context = {
        'data1': data_female,
        'data2': data_user,
        'datalist': datalist,
        'page_string': page_string
    }

    return render(request, 'blindbox_list_female.html', context)


def blindbox_male(request):
    page = int(request.GET.get('page', 1))
    page_size = 18
    start = (page - 1) * page_size
    end = page * page_size
    datalist = BlindBoxData.objects.filter(gender=1)[start:end]
    # 数据总条数
    total_count = BlindBoxData.objects.filter(gender=1).count()
    # 总页数
    page_count, div = divmod(total_count, page_size)
    if div:
        page_count += 1
    # 显示前5页和后5页
    plus = 5
    if page_count <= 2 * plus + 1:
        # 页数比较少，未达到11页
        start_page = 1
        end_page = page_count
    else:
        # 页数比较多

        # 当前页<5时
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > page_count:
                start_page = page_count - 2 * plus
                end_page = page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 页码列表
    page_str_list = []
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 下一页
    if page < page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page_count)
    page_str_list.append(prev)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(page_count))

    search_string = """
           <li>
               <form style="float: left;margin-left: -1px" method="get">
                   <div class="input-group" style="width: 200px">
                       <input type="text" name="page" class="form-control" placeholder="页码" 
                              style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                       <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                   </div>
               </form>
           </li>
           """
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {
        'datalist': datalist,
        'page_string': page_string,
    }
    return render(request, 'blindbox_male.html', context)


def blindbox_female(request):
    page = int(request.GET.get('page', 1))
    page_size = 18
    start = (page - 1) * page_size
    end = page * page_size
    datalist = BlindBoxData.objects.filter(gender=2)[start:end]
    # 数据总条数
    total_count = BlindBoxData.objects.filter(gender=2).count()
    # 总页数
    page_count, div = divmod(total_count, page_size)
    if div:
        page_count += 1
    # 显示前5页和后5页
    plus = 5
    if page_count <= 2 * plus + 1:
        # 页数比较少，未达到11页
        start_page = 1
        end_page = page_count
    else:
        # 页数比较多

        # 当前页<5时
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > page_count:
                start_page = page_count - 2 * plus
                end_page = page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 页码列表
    page_str_list = []
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 下一页
    if page < page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page_count)
    page_str_list.append(prev)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(page_count))

    search_string = """
               <li>
                   <form style="float: left;margin-left: -1px" method="get">
                       <div class="input-group" style="width: 200px">
                           <input type="text" name="page" class="form-control" placeholder="页码" 
                                  style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                           <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                       </div>
                   </form>
               </li>
               """
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {
        'datalist': datalist,
        'page_string': page_string,
    }
    return render(request, 'blindbox_female.html', context)


def blindbox_detail(request, nid):
    if request.method == 'GET':
        comment_count = BlindboxComment.objects.filter(blind_box_id=nid).count()
        # comment_content = BlindboxComment.objects.filter(blind_box_id=nid).values('content').first()['content']# 取字典的值,
        # comment_time = BlindboxComment.objects.filter(blind_box_id=nid).values('created_at').first()['created_at']
        datalist = BlindboxComment.objects.filter(blind_box_id=nid).all()
        user_now = request.session['info']['username']
        row_objects = BlindBoxData.objects.filter(id=nid).all()
        id_up = nid - 1
        id_down = nid + 1
        context = {
            'comment_count': comment_count,
            # 'comment_content': comment_content,
            'datalist': datalist,
            'row_objects': row_objects,
            'id_up': id_up,
            'id_down': id_down,
            'user_now': user_now,
        }
        return render(request, 'blindbox_detail.html', context)

    content = request.POST.get('content')
    BlindboxComment.objects.create(content=content, blind_box_id=nid)

    user_now = request.session['info']['username']
    latest_id = BlindboxComment.objects.order_by('-id').values('id').first()['id']  # 获取最后一条数据的id
    BlindboxComment.objects.filter(id=latest_id).update(user=user_now)

    return redirect('/blindbox/{}/detail/'.format(nid))


from app01.utils.encrypt import md5


class UserRegisterForm(BootstrapModelform):
    username = forms.CharField(label='用户名', required=True)
    password = forms.CharField(max_length=100, label='密码', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=100, label='再次输入密码', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='邮箱')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def register(request):
    """注册"""
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password']
            password2 = md5(form.cleaned_data['password2'])
            if User.objects.filter(username=username).exists():
                form.add_error('username', '用户名已存在')
            elif password1 != password2:
                form.add_error('password2', '两次密码不一致')
            else:
                form.save()
                return redirect('login')
        return render(request, 'register.html', {'form': form})


class UserLoginForm(BootstrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


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


def login(request):
    """登录（账号密码）"""
    if request.method == 'GET':
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    form = UserLoginForm(data=request.POST)
    if form.is_valid():
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']

        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')  # pop 不将user_input_code作为过滤条件去数据库里查找，防止出错
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "图片验证码错误")
            return render(request, 'login.html', {'form': form})

        user_object = User.objects.filter(**form.cleaned_data).first()
        # 错误
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 正确
        # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中
        request.session['info'] = {'id': user_object.id, 'username': user_object.username}
        # 7天免登录
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('index')
    return render(request, 'login.html', {'form': form})


class UserLoginEmailForm(BootstrapForm):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput,
        required=True
    )
    code = forms.CharField(
        label='邮箱验证码',
        widget=forms.TextInput,
        required=True
    )


from app01.utils.code import generate_random_code
from django.core.mail import send_mail

import json
from django.views.decorators.csrf import csrf_exempt


# 免除csrf认证

def email_code(request):
    """发邮件"""
    code = generate_random_code()
    print(request.POST)
    print(request.GET)

    # 写入session
    request.session['email_code'] = code
    # session设置60秒超时
    request.session.set_expiry(60)
    subject = '登录验证邮件'
    message = code
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.POST['email']]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    data_dict = {"status": True}
    # json_data = json.dumps(data_dict)
    # return HttpResponse(json_data)
    return JsonResponse(data_dict)



def login_email(request):
    if request.method == 'GET':
        form = UserLoginEmailForm()
        return render(request, 'login_email.html', {'form': form})

    elif request.method == 'POST':
        form = UserLoginEmailForm(data=request.POST)
        if form.is_valid():
            # 先校验验证码
            user_input_email_code = form.cleaned_data.pop('code')  # pop
            code = request.session.get('email_code', "")
            if code != user_input_email_code:
                form.add_error("code", "邮箱验证码错误")
                return render(request, 'login_email.html', {'form': form})

            user_object = User.objects.filter(**form.cleaned_data).first()
            # 错误
            if not user_object:
                form.add_error("email", "邮箱错误")
                return render(request, 'login_email.html', {'form': form})
            # 正确
            # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中
            request.session['info'] = {'id': user_object.id, 'username': user_object.username, 'email': user_object.email}
            # 7天免登录
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('index')

    form = UserLoginEmailForm(data=request.POST)
    return render(request, 'login_email.html', {'form': form})  #


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('login')


def comment(request):
    if request.method == 'GET':
        return render(request, 'comment.html', {'form': CommentForm()})

    form = CommentForm(data=request.POST)
    if form.is_valid():
        form.save()


def blindbox_placed_myself(request):
    user_now = request.session.get('info')['username']
    page = int(request.GET.get('page', 1))
    page_size = 18
    start = (page - 1) * page_size
    end = page * page_size
    datalist = BlindBoxData.objects.filter(user=user_now)[start:end]
    # 数据总条数
    total_count = BlindBoxData.objects.filter(user=user_now).count()
    # 总页数
    page_count, div = divmod(total_count, page_size)
    if div:
        page_count += 1
    # 显示前5页和后5页
    plus = 5
    if page_count <= 2 * plus + 1:
        # 页数比较少，未达到11页
        start_page = 1
        end_page = page_count
    else:
        # 页数比较多

        # 当前页<5时
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > page_count:
                start_page = page_count - 2 * plus
                end_page = page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 页码列表
    page_str_list = []
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 下一页
    if page < page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page_count)
    page_str_list.append(prev)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(page_count))

    search_string = """
               <li>
                   <form style="float: left;margin-left: -1px" method="get">
                       <div class="input-group" style="width: 200px">
                           <input type="text" name="page" class="form-control" placeholder="页码" 
                                  style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                           <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                       </div>
                   </form>
               </li>
               """
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))

    context = {
        'datalist': datalist,
        'page_string': page_string,
        'user': user_now,
    }
    return render(request, 'blindbox_placed_myself.html', context)


def blindbox_random_chose(request):
    drawn_ids = request.session.get('drawn_ids', [])

    # 从数据库中排除已抽取的ID
    queryset = BlindBoxData.objects.exclude(id__in=drawn_ids)

    # 如果还有未抽取的记录，则进行抽取
    if queryset.exists():
        # 随机抽取一个对象
        random_object = queryset.order_by('?').first()

        # 将抽取的ID添加到会话中的抽取ID列表
        drawn_ids.append(random_object.id)
        request.session['drawn_ids'] = drawn_ids

        user_now = request.session['info']['username']
        # 比较笨的方法来创造我抽取的记录
        ChosenMyself.objects.create(name=random_object.name, age=random_object.age,
                                    gender=random_object.gender, email=random_object.email,
                                    contact=random_object.contact, address=random_object.address,
                                    introduction=random_object.introduction, demand=random_object.demand,
                                    created_at=random_object.created_at, user_id=user_now)
        # 返回随机对象
        return render(request, 'blindbox_random_chose.html', {'random_object': random_object})
    else:
        # 如果所有记录都已抽取，则返回提示信息
        return render(request, 'blindbox_random_chose.html', {'message': '全都被你抽完了.'})


def blindbox_chosen_myself(request):
    user_now = request.session['info']['username']
    datalist = ChosenMyself.objects.filter(user_id=user_now)
    return render(request, 'blindbox_chosen_myself.html', {'datalist': datalist, 'user': user_now})


def blindbox_comment_delete(request):
    nid = request.GET.get("nid")
    BlindboxComment.objects.filter(id=nid).delete()
    return redirect('index')


class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

    # widgets = {
    #     'username': forms.TextInput(attrs={'class':'form-control'}),
    #     'password': forms.PasswordInput(attrs={'class':'form-control'}),
    #     'email': forms.TextInput(attrs={'class':'form-control'}),
    # }


def personal_data(request):
    if request.method == 'GET':
        form = PersonalDataForm()
        user_now = request.session['info']['username']
        data = User.objects.filter(username=user_now).all().first()
        return render(request, 'personal_data.html', {'form': form, 'data': data})
    form = PersonalDataForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse('success')
    else:
        form = PersonalDataForm()
    return render(request, 'personal_data.html', {'form': form})


def task_list(request):
    """任务列表"""
    form = UserLoginEmailForm
    return render(request, 'email_test.html', {'form': form})


# 免除csrf认证
@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST['email'])

    """发邮件"""
    code = generate_random_code()
    # 写入session
    # request.session['email_code'] = code
    # session设置60秒超时
    # request.session.set_expiry(60)
    subject = '登录验证邮件'
    message = code
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.POST['email']]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    data_dict = {"status": True, 'data': [1221312, 213]}
    json_data = json.dumps(data_dict)
    # return HttpResponse(json_data)
    return JsonResponse(data_dict)

def task_ajax1(request):
    return render(request,'index.html')