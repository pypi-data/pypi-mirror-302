import uuid


def unique_id(length=16):
    """生成随机字符串"""
    s = uuid.uuid4()
    return s.hex[:length]
