from django.db import models

# 部门模型，类名固定为Department，数据库表 app01_department（已经存在，直接复用）
class Department(models.Model):
    # 部门名称，最长32字符
    title = models.CharField(max_length=32, verbose_name="部门名称")

    class Meta:
        db_table = "app01_department"
        
    # 后台管理页面显示名称
    def __str__(self):
        return self.title


# 用户信息模型
class UserInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name="姓名")
    password = models.CharField(max_length=64, verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    # 账户金额，最大10位数字，保留2位小数
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="账户金额")
    # 创建时间
    create_time = models.DateField(verbose_name="创建时间")
    # 外键关联部门模型Department，字段名叫depart
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE, verbose_name="所属部门")
    # 性别选项
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name="性别")

    def __str__(self):
        return self.name


# 靓号模型
class PrettyNum(models.Model):
    # 号码，最长11位
    mobile = models.CharField(max_length=11, verbose_name="号码")
    # 价格
    price = models.IntegerField(verbose_name="价格", default=0)
    # 级别选项
    level_choices = ((1, "1级"), (2, "2级"), (3, "3级"), (4, "4级"))
    level = models.SmallIntegerField(choices=level_choices, verbose_name="级别", default=1)
    # 状态选项
    status_choices = ((1, "已占用"), (2, "未占用"))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态", default=2)

    def __str__(self):
        return self.mobile


# 管理员模型
class Admin(models.Model):
    # 用户名
    username = models.CharField(max_length=32, verbose_name="用户名")
    # 密码（数据库中保存md5加密后的密文）
    password = models.CharField(max_length=64, verbose_name="密码")

    def __str__(self):
        return self.username
