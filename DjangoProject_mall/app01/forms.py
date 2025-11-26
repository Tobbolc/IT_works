from django import forms
from app01.models import Buyer, Seller
from app01.utils.bootstrap import BootstrapModelform, BootstrapForm
from app01.utils.encrypt import md5
from ckeditor.fields import RichTextFormField

class BuyerRegisterForm(BootstrapModelform):
    username = forms.CharField(label='用户名', required=True)
    password = forms.CharField(max_length=100, label='密码', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=100, label='再次输入密码', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='邮箱')
    phone = forms.CharField(label="手机号码", required=True)

    class Meta:
        model = Buyer
        fields = ['username', 'email', 'password', 'phone']

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class SellerRegisterForm(BootstrapModelform):
    store_name = forms.CharField(label='店铺名称', required=True)
    seller_name = forms.CharField(label='联系人姓名', required=True)
    password = forms.CharField(max_length=100, label='密码', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=100, label='再次输入密码', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='邮箱')
    phone = forms.CharField(label="手机号码", required=True)

    class Meta:
        model = Seller
        fields = ['store_name', 'seller_name', 'email', 'password', 'phone']

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class BuyerLoginForm(BootstrapForm):
    username = forms.CharField(
        label='买家用户名',
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='图片验证码',
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class SellerLoginForm(BootstrapForm):
    store_name = forms.CharField(
        label='店铺名称',
        widget=forms.TextInput,
        required=True
    )
    # seller_name = forms.CharField(
    #     label='负责人姓名',
    #     widget=forms.TextInput,
    #     required=True
    # )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='图片验证码',
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class ForgetpwdForm(BootstrapForm):
    # username = forms.CharField(
    #     label='',
    #     widget=forms.TextInput,
    #     required=True
    # )
    code = forms.CharField(
        label='邮箱验证码',
        widget=forms.TextInput,
        required=True
    )
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['readonly'] = True


class ChangepwdForm(BootstrapForm):
    password_old = forms.CharField(
        label='旧密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    password_new = forms.CharField(
        label='新密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class BuyerInfoForm(BootstrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )
    phone = forms.CharField(
        label='手机号码',
        widget=forms.TextInput,
        required=True
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput,
        required=True
    )


class BuyerRechargeForm(BootstrapForm):
    account = forms.CharField(
        label='充值金额',
        widget=forms.Textarea,  # 记忆
        required=True
    )


class AddCommodityForm(BootstrapForm):
    name = forms.CharField(
        label='商品名',
        widget=forms.TextInput,
        required=True
    )
    price = forms.DecimalField(
        label='商品现价',
        widget=forms.TextInput,
        required=True
    )
    price_b = forms.DecimalField(
        label='商品原价',
        widget=forms.TextInput,
        required=True
    )
    stock = forms.IntegerField(
        label='库存量',
        widget=forms.TextInput,
        required=True
    )


class DetailForm(BootstrapForm):
    detail = RichTextFormField(label="详情", config_name='default')




