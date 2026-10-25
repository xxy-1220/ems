import hashlib


# md5加密，用于管理员密码保存
def md5(data_string):
    obj = hashlib.md5(data_string.encode("utf-8"))
    return obj.hexdigest()
