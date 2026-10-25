# 联通用户管理系统（EMS）

基于 **Django + MySQL** 开发的联通业务后台管理系统，包含管理员、部门、用户和靓号四个业务模块，提供完整的增删改查、搜索与分页功能。界面使用 Bootstrap 3 构建，风格统一、操作简洁。

## 功能特性

### 管理员管理
- 管理员列表：用户名关键字搜索、分页显示
- 新建管理员：用户名、密码、确认密码，密码使用 **MD5** 加密后入库
- 编辑管理员：仅允许修改用户名，密码不可编辑
- 重置密码：新密码不能与旧密码相同，两次输入必须一致
- 删除管理员：带二次确认

### 部门管理
- 部门列表、新增、编辑、删除
- 按部门名称模糊搜索
- 列表分页

### 用户管理
- 用户列表、新增、编辑、删除
- 基于 `ModelForm` 自动生成表单并进行数据校验
- 按姓名模糊搜索
- 列表分页

### 靓号管理
- 靓号列表、新增、编辑、删除
- 号码必须为 11 位数字（自定义校验）
- 按号码模糊搜索
- 支持级别（1~4 级）与状态（已占用/未占用）管理

### 任务管理
- 预留导航入口与页面，后续可扩展任务相关功能

## 技术栈

| 技术 | 版本 |
| --- | --- |
| Python | 3.x |
| Django | 4.2 |
| MySQL | 5.7+ / 8.0 |
| mysqlclient | 2.3.0 |
| Bootstrap | 3.4.1 |
| jQuery | 2.1.4 / 3.6.0 |

## 项目结构

```text
ems/
├── app01/
│   ├── middleware/          # 中间件目录
│   ├── migrations/          # 数据库迁移文件
│   ├── static/              # 静态资源（Bootstrap、jQuery、图片）
│   ├── templates/           # 页面模板
│   ├── utils/
│   │   ├── bootstrap.py
│   │   ├── code.py
│   │   ├── encrypt.py       # MD5 加密工具
│   │   ├── form.py          # BootstrapModelForm 基类
│   │   └── pagination.py    # 分页组件
│   ├── views/
│   │   ├── account.py
│   │   ├── admin.py         # 管理员模块视图
│   │   ├── depart.py        # 部门模块视图
│   │   ├── pretty.py        # 靓号模块视图
│   │   ├── task.py          # 任务模块视图
│   │   └── user.py          # 用户模块视图
│   ├── admin.py
│   ├── apps.py
│   └── models.py            # 数据模型
├── ems/
│   ├── settings.py          # 项目配置
│   ├── urls.py              # 路由配置
│   ├── asgi.py
│   └── wsgi.py
└── manage.py
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/xxy-1220/ems.git
cd ems
```

### 2. 创建虚拟环境并安装依赖

Windows：

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install django==4.2 mysqlclient==2.3.0
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django==4.2 mysqlclient==2.3.0
```

### 3. 创建数据库

```sql
CREATE DATABASE ems CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

然后修改 `ems/settings.py` 中的数据库配置：

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ems",          # 数据库名
        "USER": "root",         # 数据库用户名
        "PASSWORD": "123456",   # 数据库密码
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

### 4. 执行迁移并启动

```bash
python manage.py migrate
python manage.py runserver
```

浏览器访问：

- 管理员管理：<http://127.0.0.1:8000/admin/list/>
- 部门管理：<http://127.0.0.1:8000/depart/list/>
- 用户管理：<http://127.0.0.1:8000/user/list/>
- 靓号管理：<http://127.0.0.1:8000/pretty/list/>
- 任务管理：<http://127.0.0.1:8000/task/list/>

### 5. 默认管理员账号

| 用户名 | 密码 |
| --- | --- |
| yyy | 123456 |

> 数据库中保存的是密码的 MD5 密文，首次使用后建议通过「重置密码」功能修改密码。

## 主要路由

| 模块 | 路径 | 说明 |
| --- | --- | --- |
| 管理员 | `/admin/list/` | 管理员列表 |
| 管理员 | `/admin/add/` | 新建管理员 |
| 管理员 | `/admin/edit/<id>/` | 编辑管理员 |
| 管理员 | `/admin/reset/<id>/` | 重置密码 |
| 管理员 | `/admin/delete/<id>/` | 删除管理员 |
| 部门 | `/depart/list/` | 部门列表 |
| 部门 | `/depart/add_modelform/` | 新建部门 |
| 部门 | `/depart/edit/<id>/` | 编辑部门 |
| 部门 | `/depart/delete/<id>/` | 删除部门 |
| 用户 | `/user/list/` | 用户列表 |
| 用户 | `/user/add/` | 新建用户 |
| 用户 | `/user/add_modelform/` | 新建用户（ModelForm） |
| 用户 | `/user/edit/<id>/` | 编辑用户 |
| 用户 | `/user/delete/<id>/` | 删除用户 |
| 靓号 | `/pretty/list/` | 靓号列表 |
| 靓号 | `/pretty/add/` | 新建靓号 |
| 靓号 | `/pretty/edit/<id>/` | 编辑靓号 |
| 靓号 | `/pretty/delete/<id>/` | 删除靓号 |
| 任务 | `/task/list/` | 任务列表 |

## 说明

- 密码使用 MD5 加密存储，列表中统一显示为 `******`
- 所有列表页均支持搜索与分页，分页组件位于 `app01/utils/pagination.py`
- 页面模板采用独立页面结构，未使用母版继承，便于单独调整各页面样式
