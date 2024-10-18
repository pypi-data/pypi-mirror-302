# xy_string

- [简体中文](readme/README_zh_CN.md)
- [繁体中文](readme/README_zh_TW.md)
- [English](readme/README_en.md)


# 说明
字符串工具.

## 源码仓库

- <a href="https://github.com/xy-base/xy_string.git" target="_blank">Github地址</a>  
- <a href="https://gitee.com/xy-base/xy_string.git" target="_blank">Gitee地址</a>


## 安装

```bash
pip install xy_string
```

## 开始

```python
from xy_string.utils import is_empty_string, empty_string, contains_zh

is_empty_string("")
# true

is_empty_string("empty")
# false

empty_string("empty")
# empty

empty_string(None, default="empty")
# empty

empty_string(None)
# None

contains_zh("中文")
# True

contains_zh("Chinese")
# False

```


## 捐赠

如果小伙伴们觉得这些工具还不错的话，能否请咱喝一杯咖啡呢?  

![Pay-Total](./readme/Pay-Total.png)


## 联系方式

```
微信: yuyangiit
邮箱: 845262968@qq.com
```