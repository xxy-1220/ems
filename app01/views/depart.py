from django.shortcuts import render, redirect, get_object_or_404
from django import forms
# 导入模型：部门表Department、用户表UserInfo
from ..models import Department, UserInfo, PrettyNum
from ..utils.pagination import Pagination
from app01 import models


# ========== depart部门相关视图（视图函数/模板名字保持depart，模型类是Department） ==========
class DepartModelForm(forms.ModelForm):
    class Meta:
        # 关联数据库模型Department
        model = Department
        # 只展示部门名称字段
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        # 调用父类初始化
        super().__init__(*args, **kwargs)
        # 循环字段，统一加上bootstrap表单样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


def depart_add_modelform(request):
    if request.method == "GET":
        form = DepartModelForm()
        return render(request, "depart_add_modelform.html", {"form": form})
    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/depart/list/")
    return render(request, "depart_add_modelform.html", {"form": form})


# depart部门列表
def depart_list(request):
    """部门列表 + 搜索 + 分页"""
    #获取搜索关键词q
    search_key = request.GET.get("q", "")
    # 判断是否有搜索内容，拼接查询条件
    if search_key:
        # 模糊匹配部门名称
        queryset = models.Department.objects.filter(title__contains=search_key).order_by("id")
    else:
        # 无搜索，查全部
        queryset = models.Department.objects.all().order_by("id")

    # 实例化分页对象，每页10条
    page_obj = Pagination(request, queryset)

    context = {
        "queryset": page_obj.page_queryset,  # 当前页的数据
        "page_html": page_obj.html(),  # 分页组件html
        "q": search_key,  # 传给前端回填搜索框
    }
    # ✅ 修复：直接传context
    return render(request, "depart_list.html", context)


# 新增部门
def depart_add(request):
    # GET：打开新增页面
    if request.method == "GET":
        form = DepartModelForm()
        return render(request, "depart_add.html", {"form": form})
    # POST：提交表单保存
    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        # 保存成功跳转到部门列表
        return redirect("/depart/list/")
    # 校验失败返回页面，展示错误信息
    return render(request, "depart_add.html", {"form": form})


# 编辑部门
def depart_edit(request, nid):
    # 根据id查找部门记录，找不到返回404
    row = get_object_or_404(Department, id=nid)
    # GET：打开编辑页面，回填原有数据
    if request.method == "GET":
        form = DepartModelForm(instance=row)
        return render(request, "depart_edit.html", {"form": form})
    # POST：提交修改
    form = DepartModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/depart/list/")
    return render(request, "depart_edit.html", {"form": form})


# 删除部门
def depart_delete(request, nid):
    # 删除对应id的部门
    Department.objects.filter(id=nid).delete()
    # 删除完成跳转部门列表
    return redirect("/depart/list/")
