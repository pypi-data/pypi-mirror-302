"""系统配置"""

import os
from typing import OrderedDict
import dotenv

_CONFIG_DATA = OrderedDict()


def config(key, default=""):
    """获取.env配置内容

    Parameters
    ------------
    key
        str 配置key

    default
        any 默认值

    Returns
    ------------
    any
    """

    global _CONFIG_DATA

    if not _CONFIG_DATA:
        _CONFIG_DATA = dotenv.dotenv_values(dotenv.find_dotenv(os.environ.get("CONFIG_FILE")))

    return _CONFIG_DATA.get(key, default)
