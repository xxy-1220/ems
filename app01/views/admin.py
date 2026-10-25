from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from app01 import models
from app01.utils.form import BootstrapModelForm
from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination


# ========== 管理员相关表单 ==========
# 新建管理员：用户名、密码、确认密码
class AdminAddModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        labels = {
            "username": "用户名",
            "password": "密码",
        }
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    # 校验两次密码是否一致
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("密码不一致")
        return confirm_password

    # 保存时对密码做md5加密
    def save(self, commit=True):
        admin_object = super().save(commit=False)
        admin_object.password = md5(admin_object.password)
        if commit:
            admin_object.save()
        return admin_object


# 编辑管理员：只允许修改用户名，不允许修改密码
class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]
        labels = {
            "username": "用户名",
        }


# 重置密码：密码、确认密码
class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = models.Admin
        fields = ["password"]
        labels = {
            "password": "密码",
        }
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    # 校验新密码不能和原密码相同
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if md5(password) == self.instance.password:
            raise forms.ValidationError("不能与以前的密码相同")
        return password

    # 校验两次密码是否一致
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("密码不一致")
        return confirm_password

    # 保存时对密码做md5加密
    def save(self, commit=True):
        admin_object = super().save(commit=False)
        admin_object.password = md5(admin_object.password)
        if commit:
            admin_object.save()
        return admin_object


# ========== 管理员相关视图 ==========
# 管理员列表（支持用户名搜索 + 分页）
def admin_list(request):
    search_key = request.GET.get("q", "")
    if search_key:
        queryset = models.Admin.objects.filter(username__contains=search_key).order_by("id")
    else:
        queryset = models.Admin.objects.all().order_by("id")

    page_obj = Pagination(request, queryset)
    context = {
        "queryset": page_obj.page_queryset,
        "page_html": page_obj.html(),
        "q": search_key,
    }
    return render(request, "admin_list.html", context)


# 新建管理员
def admin_add(request):
    if request.method == "GET":
        form = AdminAddModelForm()
        return render(request, "change.html", {"form": form, "title": "新建管理员"})
    form = AdminAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": "新建管理员"})


# 编辑管理员（只能改用户名）
def admin_edit(request, nid):
    row = get_object_or_404(models.Admin, id=nid)
    if request.method == "GET":
        form = AdminEditModelForm(instance=row)
        return render(request, "change.html", {"form": form, "title": "编辑管理员"})
    form = AdminEditModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": "编辑管理员"})


# 删除管理员
def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


# 重置密码
def admin_reset(request, nid):
    row = get_object_or_404(models.Admin, id=nid)
    if request.method == "GET":
        form = AdminResetModelForm(instance=row)
        return render(request, "change.html", {"form": form, "title": f"重置密码 - {row.username}"})
    form = AdminResetModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": f"重置密码 - {row.username}"})
