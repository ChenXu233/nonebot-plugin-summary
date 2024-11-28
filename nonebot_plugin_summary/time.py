from datetime import datetime
from zoneinfo import ZoneInfo
from .config import plugin_config

def get_datetime_fromisoformat_with_timezone(date_string: str) -> datetime:
    """从 ISO-8601 格式字符串中获取时间，并包含时区信息"""
    if not plugin_config.timezone:
        return datetime.fromisoformat(date_string).astimezone()
    raw = datetime.fromisoformat(date_string)
    return (
        raw.astimezone(ZoneInfo(plugin_config.timezone))
        if raw.tzinfo
        else raw.replace(tzinfo=ZoneInfo(plugin_config.timezone))
    )

def get_datetime_now_with_timezone() -> datetime:
    """获取当前时间，并包含时区信息"""
    if plugin_config.timezone:
        return datetime.now(ZoneInfo(plugin_config.timezone))
    else:
        return datetime.now().astimezone()