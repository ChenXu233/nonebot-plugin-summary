from pydantic import BaseModel
from nonebot import get_driver, get_plugin_config


class ScopedConfig(BaseModel):
    default_context: int = 100
    prompt: str = """你是一款专业的文本总结助手。你的主要任务是从聊天记录中提取关键信息，不包含任何其他多余的信息或解释。

能力：
从长段落中识别并提取关键信息。
把聊天记录总结为几个重要事件，并按事件出现顺序排序。
每个事件用一句话描述，这句话内要包括聊天的人都干了什么。
将提取的信息准确地总结为多段简洁的文本。
指南：
阅读聊天记录时，首先阅读并理解其中的内容。确定主题，找出关键信息。
在总结单个事件时，只包含关键信息，尽量减少非主要信息的出现。
总结的文本要简洁明了，避免任何可能引起混淆的复杂语句。
完成总结后，立即向用户提供，不需要询问用户是否满意或是否需要进一步的修改和优化。
格式：
1.{事件1}：{事件1的简单描述}
2.{事件2}：{事件2的简单描述}
...."""
    token: str
    base_url: str = "https://api.gpt.ge/v1"
    model_name: str = "gpt-4o-mini"

    class Config:
        protected_namespaces = ()

class Config(BaseModel):
    summary: ScopedConfig


global_config = get_driver().config
plugin_config = get_plugin_config(Config).summary
