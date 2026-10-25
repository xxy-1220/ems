# 联通用户管理系统（EMS）

基于 **Django 4.2 + MySQL** 开发的联通业务后台管理系统。系统采用 Bootstrap 3 构建统一界面，包含 **管理员管理、部门管理、用户管理、靓号管理** 四个完整业务模块，以及预留的任务管理入口，所有模块均支持增删改查、关键字搜索和分页。

---

## 目录

- [功能概览](#功能概览)
- [管理员管理](#管理员管理)
- [部门管理](#部门管理)
- [用户管理](#用户管理)
- [靓号管理](#靓号管理)
- [任务管理](#任务管理)
- [技术栈](#技术栈)
- [数据模型](#数据模型)
- [项目结构](#项目结构)
- [核心实现说明](#核心实现说明)
- [快速开始](#快速开始)
- [路由一览](#路由一览)
- [使用指南](#使用指南)
- [常见问题](#常见问题)
- [后续规划](#后续规划)

---

## 功能概览

| 模块 | 列表 | 新增 | 编辑 | 删除 | 搜索 | 分页 | 特殊功能 |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | --- |
| 管理员管理 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 重置密码、MD5 加密 |
| 部门管理 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| 用户管理 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ModelForm 校验 |
| 靓号管理 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 号码格式校验 |
| 任务管理 | ✅ | — | — | — | — | — | 预留扩展 |

---

## 管理员管理

用于维护系统后台管理员账号，入口为 `/admin/list/`。

### 列表页
- 表格列：ID、用户名、密码、重置密码、操作
- 密码统一显示为 `******`，不展示明文或密文
- 支持按 **用户名** 关键字模糊搜索（`username__contains`）
- 每页 5 条，分页组件支持首页、上一页、页码、下一页、尾页，搜索条件在翻页时自动保留

### 新建管理员
- 表单字段：用户名、密码、确认密码
- 密码框为 `PasswordInput`，输入内容显示为圆点
- 提交前自动校验两次密码是否一致，不一致提示「密码不一致」
- 保存时通过 `md5()` 将密码转换为 32 位密文后写入数据库，数据库中不保存明文

### 编辑管理员
- 只显示「用户名」一个字段，可修改
- 密码不可在本页面修改，避免误改；如需修改密码请使用「重置密码」

### 重置密码
- 页面标题为「重置密码 - 用户名」
- 字段：新密码、确认密码
- 校验规则：
  1. 新密码的 MD5 值不能与数据库中的原密码相同，否则提示「不能与以前的密码相同」
  2. 两次输入必须一致，否则提示「密码不一致」
- 保存时同样进行 MD5 加密

### 删除管理员
- 点击「删除」弹出 `confirm` 确认框，确认后删除并返回列表

---

## 部门管理

用于维护公司部门信息，入口为 `/depart/list/`。

- **列表页**：表格列 ID、部门名称、操作；支持按部门名称模糊搜索与分页
- **新建部门**：页面标题「新建部门」，仅需填写部门名称（最长 32 个字符）
- **编辑部门**：自动回填原部门名称，可修改后保存
- **删除部门**：确认后删除，返回列表

> 部门是用户表的外键关联对象，删除部门会级联删除该部门下的用户（`on_delete=models.CASCADE`），操作前请确认。

---

## 用户管理

用于维护联通用户资料，入口为 `/user/list/`。

### 列表页
- 表格展示用户信息，支持按 **姓名** 模糊搜索
- 每页 5 条，带分页

### 新建用户
提供两种入口，表单与数据模型一致：

1. **新建用户**（`/user/add/`）
2. **新建用户ModelForm**（`/user/add_modelform/`）

表单字段说明：

| 字段 | 说明 | 组件/规则 |
| --- | --- | --- |
| 姓名 | 用户姓名 | 文本框，最长 16 字符 |
| 密码 | 登录密码 | 密码框；长度不少于 6 位，且必须同时包含字母和数字 |
| 年龄 | 用户年龄 | 数字输入 |
| 账户余额 | 账户金额 | 默认值为 `0`，最多 10 位、保留 2 位小数 |
| 入职时间 | 入职日期 | 日期选择控件（`type="date"`），数据库中对应 `create_time` |
| 性别 | 男 / 女 | 下拉选择（1=男，2=女） |
| 部门 | 所属部门 | 下拉选择，选项来自部门表 |

- 表单基于 `UserModelForm`（`ModelForm`）自动生成
- 所有输入框统一附加 Bootstrap 的 `form-control` 样式
- 校验失败时在对应字段旁显示红色错误提示，已填写内容不会丢失

### 编辑用户
- 根据用户 ID 查询记录，不存在时返回 404
- 打开页面自动回填原始数据，可修改全部字段
- 保存成功后返回用户列表

### 删除用户
- 点击「删除」并确认后删除记录，返回列表

---

## 靓号管理

用于管理可销售的手机靓号资源，入口为 `/pretty/list/`。

### 列表页
- 顶部左侧为绿色「＋ 新建靓号」按钮，右侧为搜索框（`Search for...`）
- 表格列：ID、号码、价格、级别、状态、操作
- 级别显示为「1级 / 2级 / 3级 / 4级」，状态显示为「已占用 / 未占用」
- 支持按 **号码** 模糊搜索，搜索参数为 `?q=关键字`
- 每页 5 条，搜索结果翻页时保留关键字

### 新建靓号
- 字段：号码、价格、级别、状态
- 号码校验：必须为 **11 位纯数字**，否则提示「号码必须为11位数字」
- 级别默认「1级」，状态默认「未占用」，价格默认 0
- 提交成功后返回靓号列表

### 编辑靓号
- 自动回填原号码、价格、级别、状态，可修改后保存

### 删除靓号
- 点击「删除」弹出确认框，确认后删除并返回列表

---

## 任务管理

- 入口为 `/task/list/`，已在所有页面导航栏中提供入口
- 当前为预留页面（显示暂无任务），后续可在 `app01/views/task.py` 和 `task_list.html` 基础上扩展任务的新增、编辑、删除等功能

---

## 技术栈

| 技术 | 版本/说明 |
| --- | --- |
| Python | 3.10+（本项目在 3.14 下运行） |
| Django | 4.2 |
| MySQL | 5.7 / 8.0 |
| mysqlclient | 2.3.0（MySQL 驱动） |
| Bootstrap | 3.4.1（本地静态资源） |
| jQuery | 3.6.0（本地静态资源） |
| 模板引擎 | Django Templates（各页面独立模板） |
| 密码存储 | MD5（管理员密码） |

---

## 数据模型

### Department（部门）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自增 |
| title | CharField(32) | 部门名称 |

- 数据库表名：`app01_department`（通过 `db_table` 指定）

### UserInfo（用户）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自增 |
| name | CharField(16) | 姓名 |
| password | CharField(64) | 密码 |
| age | IntegerField | 年龄 |
| account | DecimalField(10, 2) | 账户金额 |
| create_time | DateField | 入职/创建日期 |
| depart | ForeignKey → Department | 所属部门（级联删除） |
| gender | SmallIntegerField | 性别（1=男，2=女） |

### PrettyNum（靓号）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自增 |
| mobile | CharField(11) | 号码 |
| price | IntegerField | 价格，默认 0 |
| level | SmallIntegerField | 级别（1~4 级），默认 1 |
| status | SmallIntegerField | 状态（1=已占用，2=未占用），默认 2 |

### Admin（管理员）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自增 |
| username | CharField(32) | 用户名 |
| password | CharField(64) | 密码（MD5 密文） |

---

## 项目结构

```text
ems/
├── app01/
│   ├── middleware/              # 中间件目录（预留）
│   ├── migrations/              # 数据库迁移文件
│   ├── static/                  # 静态资源
│   │   ├── plugins/bootstrap-3.4.1/   # Bootstrap 的 css/js/fonts
│   │   ├── js/jquery-3.6.0.min.js
│   │   └── img/
│   ├── templates/               # 页面模板
│   │   ├── admin_list.html      # 管理员列表
│   │   ├── change.html         # 管理员新增/编辑/重置密码共用表单页
│   │   ├── depart_list.html
│   │   ├── depart_add.html
│   │   ├── depart_add_modelform.html
│   │   ├── depart_edit.html
│   │   ├── user_list.html
│   │   ├── user_add.html
│   │   ├── user_add_modelform.html
│   │   ├── user_edit.html
│   │   ├── pretty_list.html
│   │   ├── pretty_add.html
│   │   ├── pretty_edit.html
│   │   └── task_list.html
│   ├── utils/
│   │   ├── bootstrap.py         # 预留
│   │   ├── code.py              # 预留
│   │   ├── encrypt.py           # MD5 加密
│   │   ├── form.py              # BootstrapModelForm 基类
│   │   └── pagination.py        # 通用分页组件
│   ├── views/
│   │   ├── account.py          # 预留
│   │   ├── admin.py            # 管理员模块视图与表单
│   │   ├── depart.py           # 部门模块视图与表单
│   │   ├── pretty.py           # 靓号模块视图与表单
│   │   ├── task.py             # 任务模块视图
│   │   └── user.py             # 用户模块视图与表单
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   └── models.py               # 全部数据模型
├── ems/
│   ├── settings.py             # 数据库、应用、模板等配置
│   ├── urls.py                 # 全部路由
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
└── README.md
```

---

## 核心实现说明

### 1. ModelForm 表单
- 用户、部门、靓号均使用 `ModelForm`，根据模型自动生成字段和基础校验
- 管理员模块基于 `app01/utils/form.py` 中的 `BootstrapModelForm`，统一为所有字段追加 `form-control` 样式
- 自定义校验通过 `clean_字段名` 实现，例如：
  - `UserModelForm.clean_password`：密码长度和字符组成校验
  - `PrettyModelForm.clean_mobile`：11 位纯数字校验
  - `AdminResetModelForm.clean_password`：新密码不能与旧密码相同

### 2. 密码加密
`app01/utils/encrypt.py` 提供 `md5()` 函数，管理员新建和重置密码时在 `save()` 中统一加密，数据库中仅保存 32 位密文。

### 3. 搜索与分页
- 搜索：`request.GET.get("q")` + `字段__contains` 模糊查询，关键字回填到搜索框
- 分页：`app01/utils/pagination.py` 中的 `Pagination` 类，默认每页 5 条
- 分页链接会自动携带 `q` 参数，翻页后搜索条件不丢失
- 页码非法（非数字）时自动回退到第 1 页

### 4. 模板与静态资源
- 各页面为独立 HTML，不使用母版继承，便于单独调整样式
- Bootstrap 与 jQuery 使用 `app01/static/` 下的本地文件，不依赖外网 CDN
- 页面导航栏统一包含五个模块入口，当前模块高亮显示

---

## 快速开始

### 环境要求
- Python 3.10 及以上
- MySQL 5.7 或 8.0
- Windows / macOS / Linux 均可

### 1. 克隆项目

```bash
git clone https://github.com/xxy-1220/ems.git
cd ems
```

### 2. 创建并激活虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install django==4.2 mysqlclient==2.3.0
```

### 4. 创建数据库

登录 MySQL 后执行：

```sql
CREATE DATABASE ems CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

### 5. 修改数据库配置

编辑 `ems/settings.py`，将数据库连接信息改为本机实际配置：

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ems",          # 数据库名
        "USER": "root",         # 数据库用户名
        "PASSWORD": "123456",   # 数据库密码
        "HOST": "127.0.0.1",    # 数据库地址
        "PORT": "3306",         # 端口
    }
}
```

### 6. 执行数据库迁移

```bash
python manage.py migrate
```

该命令会创建 `app01_department`、`app01_userinfo`、`app01_prettynum`、`app01_admin` 等表。

### 7. 启动开发服务器

```bash
python manage.py runserver
```

看到 `Starting development server at http://127.0.0.1:8000/` 即启动成功。

### 8. 访问系统

| 模块 | 地址 |
| --- | --- |
| 管理员管理 | <http://127.0.0.1:8000/admin/list/> |
| 部门管理 | <http://127.0.0.1:8000/depart/list/> |
| 用户管理 | <http://127.0.0.1:8000/user/list/> |
| 靓号管理 | <http://127.0.0.1:8000/pretty/list/> |
| 任务管理 | <http://127.0.0.1:8000/task/list/> |

### 9. 默认管理员

| 用户名 | 密码 |
| --- | --- |
| yyy | 123456 |

> 数据库保存的是密码的 MD5 密文。首次登录后建议通过「重置密码」修改默认密码。

---

## 路由一览

| 模块 | 方法 | 路径 | 功能 |
| --- | --- | --- | --- |
| 管理员 | GET | `/admin/list/` | 管理员列表（支持 `?q=` 搜索、`?page=` 分页） |
| 管理员 | GET/POST | `/admin/add/` | 新建管理员 |
| 管理员 | GET/POST | `/admin/edit/<id>/` | 编辑管理员（仅用户名） |
| 管理员 | GET/POST | `/admin/reset/<id>/` | 重置密码 |
| 管理员 | GET | `/admin/delete/<id>/` | 删除管理员 |
| 部门 | GET | `/depart/list/` | 部门列表 |
| 部门 | GET/POST | `/depart/add/` | 新建部门 |
| 部门 | GET/POST | `/depart/add_modelform/` | 新建部门（ModelForm） |
| 部门 | GET/POST | `/depart/edit/<id>/` | 编辑部门 |
| 部门 | GET | `/depart/delete/<id>/` | 删除部门 |
| 用户 | GET | `/user/list/` | 用户列表 |
| 用户 | GET/POST | `/user/add/` | 新建用户 |
| 用户 | GET/POST | `/user/add_modelform/` | 新建用户（ModelForm） |
| 用户 | GET/POST | `/user/edit/<id>/` | 编辑用户 |
| 用户 | GET | `/user/delete/<id>/` | 删除用户 |
| 靓号 | GET | `/pretty/list/` | 靓号列表 |
| 靓号 | GET/POST | `/pretty/add/` | 新建靓号 |
| 靓号 | GET/POST | `/pretty/edit/<id>/` | 编辑靓号 |
| 靓号 | GET | `/pretty/delete/<id>/` | 删除靓号 |
| 任务 | GET | `/task/list/` | 任务列表（预留） |

---

## 使用指南

### 新增一个部门
1. 进入「部门管理」→ 点击「新建部门」
2. 输入部门名称，点击「提交」
3. 自动返回部门列表，新部门出现在列表中

### 新增一个用户
1. 进入「用户管理」→ 点击「新建用户」（或「新建用户ModelForm」）
2. 填写姓名、密码、年龄、账户余额、入职时间
3. 选择性别和所属部门
4. 点击「提交」，校验通过后返回列表

> 密码需至少 6 位且同时包含字母和数字，账户余额默认 0，可按需修改。

### 添加一个靓号
1. 进入「靓号管理」→ 点击「＋ 新建靓号」
2. 输入 11 位号码、价格，选择级别和状态
3. 点击「提交」，成功后返回列表

### 搜索数据
- 在列表右上角搜索框输入关键字，点击放大镜或按回车
- 管理员按用户名搜索，部门按名称搜索，用户按姓名搜索，靓号按号码搜索
- 搜索状态会保留在分页链接中

### 重置管理员密码
1. 管理员列表点击「重置密码」
2. 输入新密码和确认密码（新密码不能与原密码相同）
3. 点击「提交」，系统自动 MD5 加密保存

---

## 常见问题

### 1. `mysqlclient` 安装失败
Windows 上若提示缺少编译环境，可尝试：

```bash
pip install --only-binary :all: mysqlclient
```

仍失败时安装 **Visual Studio Build Tools**（勾选 C++ 生成工具）后重试。也可改用 `pymysql`，并在 `ems/__init__.py` 中添加：

```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 2. 启动时报 `No module named 'MySQLdb'`
说明 MySQL 驱动未安装，执行：

```bash
pip install mysqlclient
```

### 3. 提示 `Unknown database 'ems'` 或连接失败
- 确认 MySQL 服务已启动
- 确认已执行 `CREATE DATABASE ems CHARACTER SET utf8mb4;`
- 检查 `settings.py` 中的用户名、密码、端口是否正确

### 4. 报错 `Table 'ems.app01_xxx' doesn't exist`
未执行迁移，运行：

```bash
python manage.py migrate
```

### 5. 页面样式错乱或下拉菜单点不开
- 确认 `app01/static/plugins/bootstrap-3.4.1/` 与 `app01/static/js/` 文件完整
- 开发模式下 `DEBUG = True` 才能由 Django 直接提供静态文件
- 浏览器按 `Ctrl + F5` 强制刷新，排除缓存影响

### 6. 端口 8000 被占用
```bash
python manage.py runserver 8001
```

### 7. 想清空数据并重新开始
删除对应表数据后重新迁移，例如：

```sql
TRUNCATE TABLE app01_admin;
```

如需让自增 ID 从 1 重新开始，使用 `TRUNCATE`（会重置自增计数器），或执行：

```sql
ALTER TABLE app01_admin AUTO_INCREMENT = 1;
```

---

## 后续规划

- 完善任务管理模块（任务发布、分配、状态流转）
- 增加管理员登录与权限控制
- 用户密码加密存储，替换当前明文存储方式
- 增加数据导出（Excel）与操作日志
- 将管理员的 MD5 升级为更安全的加盐哈希算法
