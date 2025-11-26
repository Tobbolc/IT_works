import datetime
import random

def generate_oid():
    """创建订单号"""
    now = datetime.datetime.now()
    # 格式化年份、月份和日
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    # 生成四位随机数字
    random_number = random.randint(1000, 9999)
    # 拼接字符串生成订单号
    order_id = f"{year}{month}{day}{random_number:04d}"
    return order_id