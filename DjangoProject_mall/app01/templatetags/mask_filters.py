# templatetags/mask_filters.py
from django import template

register = template.Library()

@register.filter
def mask_password(value):
    """密码脱敏：用 8 个星号代替"""
    return '*' * 8

@register.filter
def mask_phone(value):
    """手机号脱敏：保留前 3 位和后 4 位"""
    if len(value) >= 7:
        return value[:3] + '****' + value[-4:]
    return value

@register.filter
def mask_email(value):
    """邮箱脱敏：保留前缀前 2 位和后 2 位，域名完整显示"""
    if '@' in value:
        prefix, domain = value.split('@')
        if len(prefix) >= 4:
            masked_prefix = prefix[:2] + '****' + prefix[-2:]
            return f'{masked_prefix}@{domain}'
    return value