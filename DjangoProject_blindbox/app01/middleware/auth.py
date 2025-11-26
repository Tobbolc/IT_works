from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):
    # 读取用户访问的session信息来判断是否已登录
    def process_request(self, request):
        # 排除不需要认证就可以进入的页面，比如登录界面，否则就是死循环
        if request.path_info in ['/login/', '/register/', '/image/code/', '/login/email/', '/email/code/']:
            return
        #return None 即继续往后走
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 未登录
        return redirect('login')