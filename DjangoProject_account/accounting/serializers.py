from rest_framework import serializers
from .models import User, Category, Transaction
from accounting.utils.encrypt import md5

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # 密码不返回给前端
        required=True,
    )
    class Meta:
        model = User
        fields = ['phone','password', 'email']  # 需要前端提交的字段
        extra_kwargs = {
            "id":{'read_only':True},
            'password': {'write_only': True},  # 确保密码不会序列化输出
            'email': {'required': True},       # 强制邮箱必填
            'phone': {'required': True}
        }
    def create(self, validated_data):
        # 创建用户时自动加密密码
        user = User.objects.create(
            phone=validated_data['phone'],
            password=md5(validated_data['password']),
            email=validated_data['email']
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    password = serializers.CharField(
        # write_only=True,  # 密码不返回给前端
        required=True,
    )
    class Meta:
        model = User
        fields = ['email', 'password']  # 需要前端提交的字段
        extra_kwargs = {
            "id":{'read_only':True},
            'password': {'write_only': True},  # 确保密码不会序列化输出
            'email':{'required': True}
        }

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'user']
#         extra_kwargs = {
#             'user': {'read_only': True}
#         }

class TransactionSerializer(serializers.ModelSerializer):
    # 通过用户名关联用户（前端传递用户名，后端自动转换为 User 对象）
    username = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    # 通过交易类型名称关联 TransactionType（前端传递类型名称，后端自动转换）
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Transaction
        fields = ['username','amount', 'date', 'category']

class TransactionGetSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        slug_field='username',  # 使用 User 模型的 username 字段
        read_only=True  # 仅用于序列化输出（前端无需输入）
    )
    # 将 transaction_type 外键字段转换为类型名称
    category = serializers.SlugRelatedField(
        slug_field='name',  # 使用 category 模型的 name 字段
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = '__all__'  # 包含所有需要返回的字段

