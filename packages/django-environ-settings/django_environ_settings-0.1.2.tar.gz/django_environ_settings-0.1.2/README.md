# django-environ-settings

从环境变量中加载Django配置项。

## 安装

```shell
pip install django-environ-settings
```

## 使用方法

在`pro/settings.py`结尾处添加以下代码：

```python
from django_environ_settings import django_environ_settings_patch_all

django_environ_settings_patch_all(
    keys=["CONFIG_ITEM_KEY"],
    mapping_keys={
        "ENV_KEY1": "DJANGO_KEY1",
        "ENV_KEY2": "DJANGO_KEY2",
    }
    namespace="DJANGO_",
)
```

- `namespace="DJANGO_"`表示只有以`DJANGO_`开头的环境变量才被django使用，并用于更新移除`DJANGO_`前缀后对应的配置项。
    - 如`django`中的数据库配置项`DATABASES`对应的环境变量为`DJANGO_DATABASES`。
- `keys`用于加载不使用`namespace`前缀的环境变量。允许为空。
    - 如`CONFIG_ITEM_KEY`表示在`djaong.conf.settings`中添加了额外的`CONFIG_ITEM_KEY`配置项。
    - 当前使用`namespace`前缀的环境变量`DJANGO_CONFIG_ITEM_KEY`也能实现相同效果，并且优先级更高。
- `mapping_keys`用于处理环境变量名与`django`配置项名不一致的情况。
    - 如：把环境变量`ENV_KEY1`的值加载为`django`的`DJANGO_KEY1`配置项。
- 环境变量值使用YAML格式编写。

## 版本

### v0.1.0

- 版本首发，基本功能完成。

### v0.1.1

- 添加：内外部KEY值映射的支持。
- 修正：打包后*.whl中没有包含有效代码的问题。
- 修正：加载配置项时没有移除前缀的问题。

### v0.1.2

- 修正：需要忽略DJANGO_SETTINGS_MODULE配置项的问题。
