from django.shortcuts import render, redirect, get_object_or_404
from django import forms
# 导入模型：部门表Department、用户表UserInfo
from ..models import Department, UserInfo, PrettyNum
from ..utils.pagination import Pagination
from app01 import models

# -------------------------- ModelForm 类定义 --------------------------
# 用户的ModelForm，自动根据UserInfo模型生成表单、校验规则
class UserModelForm(forms.ModelForm):
    class Meta:
        # 绑定对应的数据库模型
        model = UserInfo
        # 指定页面上要展示的字段
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]

        labels = {
            "create_time": "入职时间",
        }

        widgets = {
            # 入职时间：日期选择框
            "create_time": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            # 性别下拉
            "gender": forms.Select(choices=[(1, "男"), (2, "女")], attrs={"class": "form-control"}),
            # 部门下拉，Django自动关联外键Department
            "depart": forms.Select(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def clean_password(self):
        # 密码校验：至少6位，字母+数字
        pwd = self.cleaned_data.get("password")
        if len(pwd) < 6:
            raise forms.ValidationError("密码长度不能少于6位")
        if not any(c.isdigit() for c in pwd):
            raise forms.ValidationError("密码必须包含数字")
        if not any(c.isalpha() for c in pwd):
            raise forms.ValidationError("密码必须包含字母")
        return pwd

    # 构造方法：给所有的表单输入框统一添加bootstrap样式class
    def __init__(self, *args, **kwargs):
        # 调用父类的初始化方法
        super().__init__(*args, **kwargs)
        # 循环所有字段，统一设置属性
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


def user_add_modelform(request):
    if request.method == "GET":
        form = UserModelForm(initial={"account": 0})
        return render(request, "user_add_modelform.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")  # 提交成功返回用户列表页
    return render(request, "user_add_modelform.html", {"form": form})


# -------------------------- 视图函数 --------------------------
# 用户列表页面
def user_list(request):
    """用户列表 + 搜索 + 分页"""
    search_key = request.GET.get("q", "")
    if search_key:
        # 按用户名模糊搜索
        queryset = models.UserInfo.objects.filter(name__contains=search_key).order_by("id")
    else:
        queryset = models.UserInfo.objects.all().order_by("id")

    page_obj = Pagination(request, queryset)
    context = {
        "queryset": page_obj.page_queryset,
        "page_html": page_obj.html(),
        "q": search_key,
    }
    # ✅ 修复：直接传context
    return render(request, "user_list.html", context)


# 新建用户
def user_add(request):
    # GET请求：打开新增页面
    if request.method == "GET":
        # 实例化空表单，账户余额默认0
        form = UserModelForm(initial={"account": 0})
        return render(request, "user_add.html", {"form": form})

    # POST请求：表单提交，保存数据
    # 获取前端提交的数据，传给form
    form = UserModelForm(data=request.POST)
    # 自动执行数据校验
    if form.is_valid():
        # 校验通过，直接保存到数据库（ModelForm核心）
        form.save()
        # 保存完成，重定向跳转到用户列表页
        return redirect("/user/list/")

    # 校验失败，返回页面，form里自带错误信息，前端展示
    return render(request, "user_add.html", {"form": form})


# 编辑用户，nid为要编辑用户的id
def user_edit(request, nid):
    # 根据id查询用户，找不到直接返回404页面
    row = get_object_or_404(UserInfo, id=nid)

    # GET请求：打开编辑页面，回填原始数据
    if request.method == "GET":
        # instance参数：把查询出来的对象传入，表单自动回填原有数据
        form = UserModelForm(instance=row)
        return render(request, "user_edit.html", {"form": form})

    # POST请求：提交修改，更新数据库
    form = UserModelForm(data=request.POST, instance=row)
    if form.is_valid():
        # 校验通过，更新数据库这条记录
        form.save()
        # 修改完成，跳转回用户列表
        return redirect("/user/list/")

    # 校验失败，返回页面并展示错误
    return render(request, "user_edit.html", {"form": form})


# 删除用户，nid为待删除用户id
def user_delete(request, nid):
    # 根据id过滤并删除记录
    UserInfo.objects.filter(id=nid).delete()
    # 删除完成，重定向到用户列表
    return redirect("/user/list/")
