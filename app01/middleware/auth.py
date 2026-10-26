from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    """
    登录校验中间件
    拦截所有请求：检查 session 中是否有 info
    """

    def process_request(self, request):
        # ========== 0. 排除不需要登录就能访问的页面 ==========
        path = request.path_info

        # 登录页面本身
        if path == "/login/":
            return
        if path == "/logout/":
            return

        # 静态资源：/static/ 开头的全部放行
        if path.startswith("/static/"):
            return

        # /favicon.ico 浏览器图标
        if path == "/favicon.ico":
            return

        # ========== 1. 读取 session ==========
        info_dict = request.session.get("info")
        if info_dict:
            # 已登录，继续向后执行
            return

        # ========== 2. 未登录，重定向到登录页 ==========
        return redirect("/login/")
