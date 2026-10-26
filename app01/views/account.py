from django.shortcuts import render, redirect

from app01 import models
from app01.utils.encrypt import md5


# ========== 登录 ==========
def login(request):
    """
    登录页面 + 登录校验
    登录成功后，把管理员信息写入 request.session["info"]
    """
    if request.method == "GET":
        return render(request, "login.html")

    # POST：校验用户名和密码
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()

    # 基础校验
    if not username or not password:
        return render(request, "login.html", {"error": "用户名和密码不能为空"})

    # 密码 md5 加密后去数据库比对
    password_md5 = md5(password)
    row = models.Admin.objects.filter(username=username, password=password_md5).first()

    if row:
        # 登录成功，把信息写入 session
        request.session["info"] = {
            "id": row.id,
            "username": row.username,
        }
        # 默认跳到管理员列表（你可以改成首页 /admin/list/）
        return redirect("/admin/list/")

    # 登录失败
    return render(request, "login.html", {"error": "用户名或密码错误"})


# ========== 注销 ==========
def logout(request):
    """
    注销登录：清空 session，跳回登录页
    """
    request.session.clear()
    return redirect("/login/")
