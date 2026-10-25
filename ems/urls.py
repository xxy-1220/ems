"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
# 按新目录结构，分别导入各模块的视图
from app01.views import user, depart, pretty, task
from app01.views import admin as admin_view

urlpatterns = [
    # 管理员相关
    path("admin/list/", admin_view.admin_list),
    path("admin/add/", admin_view.admin_add),
    path("admin/edit/<int:nid>/", admin_view.admin_edit),
    path("admin/delete/<int:nid>/", admin_view.admin_delete),
    path("admin/reset/<int:nid>/", admin_view.admin_reset),
    # 用户相关
    path("user/list/", user.user_list, name="user_list"),
    path("user/add/", user.user_add, name="user_add"),
    path("user/edit/<int:nid>/", user.user_edit, name="user_edit"),
    path("user/delete/<int:nid>/", user.user_delete, name="user_delete"),
    path("user/add_modelform/", user.user_add_modelform),
    # 部门相关（保留之前写的）
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/edit/<int:nid>/", depart.depart_edit),
    path("depart/delete/<int:nid>/", depart.depart_delete),
    # 新增ModelForm新增用户路由
    path("depart/add_modelform/", depart.depart_add_modelform),
    # 靓号相关
    path("pretty/list/", pretty.pretty_list),
    path("pretty/add/", pretty.pretty_add),
    path("pretty/edit/<int:nid>/", pretty.pretty_edit),
    path("pretty/delete/<int:nid>/", pretty.pretty_delete),
    # 任务相关
    path("task/list/", task.task_list),
]