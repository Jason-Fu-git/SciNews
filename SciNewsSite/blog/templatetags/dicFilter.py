from django import template

register = template.Library()
"""用于html模板文件中，字典查询工作"""


def key(dic, key_val):
    """
    给定键，返回值
    :param dic: 字典
    :param key_val: 键值
    :return: 返回字典中键值对应的值
    """
    key_val = int(key_val)
    if key_val in dic:
        return dic[key_val]
    else:
        return ""


register.filter("key", key)  # 注册
