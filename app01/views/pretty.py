from django.shortcuts import render, redirect, get_object_or_404
from django import forms
# 导入模型：部门表Department、用户表UserInfo
from ..models import Department, UserInfo, PrettyNum
from ..utils.pagination import Pagination
from app01 import models


# ========== 靓号相关视图 ==========
# 靓号的ModelForm
# 创建靓号ModelForm表单类，自动关联模型，用于新增、编辑靓号
class PrettyModelForm(forms.ModelForm):
    class Meta:
        # 绑定对应的模型类：PrettyNum靓号模型
        model = PrettyNum
        # 指定需要生成表单输入框的字段：手机号、价格、等级、状态
        fields = ["mobile", "price", "level", "status"]

    # 表单初始化方法，实例化表单时自动执行
    def __init__(self, *args, **kwargs):
        # 调用父类ModelForm的构造方法，完成基础初始化
        super().__init__(*args, **kwargs)
        # 循环遍历表单内所有字段
        for name, field in self.fields.items():
            # 给每一个输入框统一添加bootstrap的form-control样式类
            field.widget.attrs['class'] = 'form-control'

    # 自定义手机号校验方法，命名规则clean_字段名，form.is_valid()时自动执行
    def clean_mobile(self):
        # 获取清洗后的手机号数据
        mobile = self.cleaned_data.get("mobile")
        # 判断：不是纯数字 或者 长度不等于11位
        if not mobile.isdigit() or len(mobile) != 11:
            # 抛出表单校验错误，错误信息展示在前端页面
            raise forms.ValidationError("号码必须为11位数字")
        # 校验通过，返回手机号存入cleaned_data
        return mobile


# 靓号列表视图函数，支持手机号模糊搜索
def pretty_list(request):
    """靓号列表 + 搜索 + 分页"""
    search_key = request.GET.get("q", "")
    if search_key:
        # 按手机号模糊搜索
        queryset = models.PrettyNum.objects.filter(mobile__contains=search_key).order_by("id")
    else:
        queryset = models.PrettyNum.objects.all().order_by("id")

    page_obj = Pagination(request, queryset)
    context = {
        "queryset": page_obj.page_queryset,
        "page_html": page_obj.html(),
        "q": search_key,
    }
    # ✅ 修复：只返回context
    return render(request, "pretty_list.html", context)


# 新建靓号视图函数
def pretty_add(request):
    # GET请求：打开新增靓号页面
    if request.method == "GET":
        # 创建空表单对象
        form = PrettyModelForm()
        # 将表单传递给模板渲染输入框
        return render(request, "pretty_add.html", {"form": form})
    # POST请求：用户提交表单数据
    form = PrettyModelForm(data=request.POST)
    # form.is_valid()执行全部校验（包含自定义clean_mobile手机号校验）
    if form.is_valid():
        # 校验通过，保存数据到数据库，新增一条靓号记录
        form.save()
        # 保存成功，重定向跳转到靓号列表页面
        return redirect("/pretty/list/")
    # 校验失败，返回新增页面，页面展示错误提示
    return render(request, "pretty_add.html", {"form": form})


# 编辑靓号视图函数，nid是路由传入的靓号主键id
def pretty_edit(request, nid):
    # 根据nid查询靓号；找不到数据直接返回404页面，不会抛出程序异常
    row = get_object_or_404(PrettyNum, id=nid)
    # GET请求：打开编辑页面
    if request.method == "GET":
        # instance=row：传入数据库查询到的靓号对象，自动回填旧数据到表单
        form = PrettyModelForm(instance=row)
        return render(request, "pretty_edit.html", {"form": form})
    # POST提交修改内容，data接收前端提交数据，instance指定要修改的对象
    form = PrettyModelForm(data=request.POST, instance=row)
    if form.is_valid():
        # 校验通过，更新数据库原有记录，不会新增数据
        form.save()
        # 修改完成，跳转回靓号列表页面
        return redirect("/pretty/list/")
    # 校验失败，返回编辑页面展示错误信息
    return render(request, "pretty_edit.html", {"form": form})


# 删除靓号视图函数，nid为待删除靓号的id
def pretty_delete(request, nid):
    # 根据id筛选记录并删除；id不存在不会报错，无操作直接执行跳转
    PrettyNum.objects.filter(id=nid).delete()
    # 删除完成，重定向到靓号列表页面
    return redirect("/pretty/list/")
